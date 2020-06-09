import datetime
from flask import flash, g, jsonify, redirect, render_template, request, session, url_for
import re

from snowfort import db
from snowfort.blueprints.motes.models import Mote
from snowfort.blueprints.sensors.models import Sensor
from snowfort.blueprints.stations.models import Station
from snowfort.shared.decorators import requires_login
from snowfort.shared.utilities import to_epoch_seconds

from . import mod
from forms import DatumForm
from models import Datum


@mod.route('/new/', methods=['GET', 'POST'])
@requires_login
def new():
    """
    New datum action to create a new datum.
    """
    form = DatumForm(request.form)
    if form.validate_on_submit():
        datum = Datum(form.sensor.data.attribute, form.value.data, form.timestamp.data,
                      form.mote.data.tag, form.timeslot.data, form.axis.data, form.packet_num.data)
        db.session.add(datum)
        db.session.commit()

        flash('You have successfully added a new datum.', 'success')
        return redirect(url_for('data.view', id=datum.id))
    return render_template('data/new.html', form=form)


@mod.route('/edit/<int:id>', methods=['GET', 'POST'])
#@requires_login
def edit(id):
    """
    Edit datum form to modify a datum.
    """
    datum = Datum.query.get(id)
    form = DatumForm(request.form, obj=datum)
    if request.method == 'POST':
        form.populate_obj(datum)
        if form.validate():
            db.session.commit()
            flash('You have successfully modified the datum.', 'success')
            return redirect(url_for('data.edit', id=datum.id))
    return render_template('data/edit.html', form=form, datum=datum)


@mod.route('/view/<int:id>', methods=['GET'])
@requires_login
def view(id):
    """
    View action for showing a particular datum.
    """
    datum = Datum.query.get(id)
    if datum:
        return render_template('data/view.html', datum=datum)
    flash('Invalid datum ID of ' + str(id) + ' given!', 'danger')
    return redirect(url_for('data.all'))


@mod.route('/post', methods=['POST'])
def post():
    """
    Post data to the system.
    Example:
    {
      "station": "Stanford",
      "mote_id": "1",
      "timeslot": 1,
      "timestamp": 1394695678.0,
      "data": {
          "acc_x": [1.0, 2.0, 3.0, 4.0, 5.0],
          "acc_y": [1.0, 2.0, 3.0, 4.0, 5.0],
          "acc_z": [1.0, 2.0, 3.0, 4.0, 5.0],
          "gyro_x": [1.0, 2.0, 3.0, 4.0, 5.0],
          "gyro_y": [1.0, 2.0, 3.0, 4.0, 5.0],
          "gyro_z": [1.0, 2.0, 3.0, 4.0, 5.0],
          "temperature": [1.0, 2.0, 3.0, 4.0, 5.0]
      }
    }
    """
    data = request.json

    # Verify Data
    tags = ["station", "mote_id", "timeslot", "data", "packet_num"]
    missing = []
    for tag in tags:
        if data.get(tag) is None:
            missing.append(tag)

    if len(missing) > 0:
        print "[ERROR] Post request missing " + ", ".join(missing)
        response = {"status": "error", "message": "Missing " + ", ".join(missing)}
        return jsonify(response)

    # Get the data and produce data points
    mote_tag = "{0}-{1}".format(data["station"], data["mote_id"])
    mote = Mote.query.filter_by(tag=mote_tag).first()
    if mote is None:
        print "[ERROR] Post request missing mote of given tag " + mote_tag
        response = {"status": "error", "message": "Missing mote!"}
        return jsonify(response)

    timeslot = data["timeslot"]
    packet_num = data["packet_num"]

    if mote.last_pkt is None:
        mote.last_pkt = packet_num
        mote.received += 1
    else:
        mote.received += 1
        # Deal with missing
        # Note there are edge cases in which we loop around more than 255
        # missing in one burst
        diff = packet_num - mote.last_pkt
        if diff > 1:
            mote.missed += diff - 1
        elif diff < 0:
            mote.missed += 255 - mote.last_pkt + packet_num
        mote.last_pkt = packet_num

    end_ts = datetime.datetime.utcnow()
    if data.get("timestamp"):
        end_ts = datetime.datetime.utcfromtimestamp(float(data["timestamp"]))

    ts_offset = 1.0 / mote.sampling  # Per second
    sensors = data["data"]

    regex = re.compile("(\w+)_(\w+)")
    for sensor in sensors:  # Each of the sensor data
        m = regex.match(sensor)
        axis = None
        attribute = None
        if m:  # Have multi-axis data
            attribute = m.group(1)
            axis = m.group(2)
        else:
            attribute = sensor

        # Go through each data point and insert datum
        slen = len(sensors[sensor])
        i = 0
        for datum in sensors[sensor]:
            ts = end_ts - datetime.timedelta(seconds=((slen - i) * ts_offset))
            point = Datum(attribute, datum, ts, mote_tag, timeslot, axis, packet_num)
            print "[LOG] Adding datum %s to transaction." % (str(point))
            db.session.add(point)
            i += 1

    db.session.commit()

    response = {"status": "success"}
    print "[LOG] Successfully committed data."
    return jsonify(response)


@mod.route('/all/', methods=['GET'])
@requires_login
def all():
    """
    All action to show all data that are in the database.
    """
    data = Datum.query.order_by(Datum.timestamp.desc()).limit(100).all()
    return render_template('data/all.html', data=data)


@mod.route('/station/<int:id>',
           defaults={'attribute': None, 't_start': None, 't_end': None},
           methods=['GET'])
@mod.route('/station/<int:id>/<string:attribute>',
           defaults={'t_start': None, 't_end': None},
           methods=['GET'])
@mod.route('/station/<int:id>/<string:attribute>/<string:t_start>/<string:t_end>',
           methods=['GET'])
## deactivated login for public view
#@requires_login
def station_data(id, attribute, t_start, t_end):
    """
    API to get Station data for station with id.
    Flot Graph Library has some set data structure:
      + You must provide a hash for each line you want.
      + Each line have keys which for our purposes need to be:
        - data: An array of the data to present with format [date, value].
        - label: The label to present on the graph.
        - idx: The index to correspond with click events.

    API:
      + id: The station id that you are viewing.
      + attribute: The sensor attribute to view. (Optional)
      + start: Limit when to start value querying. (Optional)
      + end: Limit when to end value querying. (Optional)
    """
    current = datetime.datetime.utcnow()
    window = current - datetime.timedelta(minutes=5)  # View last 5 minutes of data

    station = Station.query.get(id)
    if station is None:
        response = {'data': [], 'error': 'Invalid Station id.'}
        return jsonify(response)

    if attribute is None:
        attribute = Sensor.query.get(1).attribute

    sensor = Sensor.query.filter_by(attribute=attribute).first()

    data = []
    idx = 0
    for mote in station.motes:
        if (t_start is None and t_end is None):
            # No date range so limit by hard limit
            limit_data = Datum.query.filter_by(mote_tag=mote.tag, attribute=attribute) \
                .filter(Datum.timestamp >= window) \
                .order_by(Datum.timestamp.desc())
        else:
            # There is a date range so limit
            dt_start = datetime.datetime.utcfromtimestamp(float(t_start))
            dt_end = datetime.datetime.utcfromtimestamp(float(t_end))
            limit_data = Datum.query.filter_by(mote_tag=mote.tag, attribute=attribute) \
                .filter(Datum.timestamp >= dt_start, Datum.timestamp <= dt_end) \
                .order_by(Datum.timestamp.desc())
        # Now build the results
        mote_data = {}
        for datum in limit_data:
            mote_label = mote.tag
            if datum.axis:
                mote_label += "-{0}".format(datum.axis)  # With axis then tag-axis is label

            # If data array not existing yet for axis then create
            if mote_data.get(mote_label) is None:
                mote_data[mote_label] = []

            # Convert the timestamp and use transfer function for data
            ts = to_epoch_seconds(datum.timestamp) * 1000
            y = sensor.c_1 * float(datum.value) + sensor.c_2
            mote_data[mote_label].append([ts, y])

        # Go through and make a data sample for each axis
        for mote_label in mote_data:
            data.append({'data': mote_data[mote_label],
                         'label': mote_label,
                         'idx': idx})
            idx += 1

    response = {'data': data, 'attribute': attribute}
    return jsonify(response)


###################################### Everything below added by Rebecca

from flask import Flask, send_file
import StringIO
from format_download import string_lengths, format_header, format_data, format_footer


@mod.route('/download/')
## Use this line to make a private page
## @requires_login
def download():
    attributes_by_mote = []
    sensors = []

    ## This query finds all motes and their corresponding stations by id
    ## in SQL: SELECT motes.tag, stations.name FROM stations JOIN motes ON motes.station_id=stations.id;
    motes = db.session.query(Mote.tag, Station.name).join(Station, Mote.station_id==Station.id).all()

    for mote in motes:

        ## This filters all distinct attributes for each mote
        ## in SQL: SELECT DISTINCT attribute FROM data WHERE mote_tag="...";
        attributes_data = Datum.query.filter(Datum.mote_tag == mote.tag) \
                                    .with_entities(Datum.attribute).distinct()

        for item in attributes_data:
            attributes_by_mote.append(str(item.attribute))

        sensors.append([str(mote.tag), str(mote.name), sorted(attributes_by_mote)])

        attributes_by_mote = []

    return render_template('/data/download.html', motes=motes, sensors=sorted(sensors))


@mod.route('/download_file', methods=['POST'])
## Use this line to make a private page
## @requires_login
def prepare_file():

    if request.method == 'POST':

        ## This gets the information from the checkboxes
        selected = request.form.getlist('attributes')

        ## sensors is a list of lists containing a mote_tag and an attribute
        sensors = get_sensors(selected)

        ## This gets the start and end dates
        date_start = str(request.form['date_start'])
        date_end = str(request.form['date_end'])

        ## The data is stored in a list; each item contains timestamp, mote_tag, attribute, and value
        data = []

        ## This query is for all selected motes
        for sensor in sensors:
            ## filters the data within a specific time range in ascending order
            ## asc = ascending; desc = descending
            data_item = Datum.query.filter(Datum.mote_tag == str(sensor[0]), Datum.attribute == str(sensor[1]),
                                            Datum.timestamp >= date_start,
                                           Datum.timestamp <= date_end) \
                .order_by(Datum.timestamp.asc())

            ## This extracts info and appends to data list
            for item in data_item:
                data.append({"timestamp": item.timestamp, "mote_tag": item.mote_tag, "attribute": item.attribute,
                             "value": item.value})

        ## This provides error messages if user does not select a mote, a start date, an end date, or if no data is available
        if len(selected) == 0 or date_start == "" or date_end == "" or data == []:

            flash_msgs(selected, date_start, date_end, data)

            return redirect(url_for('data.download'))

        else:

            strIO, filename = create_file(selected, date_start, date_end, data)

            return send_file(strIO, attachment_filename=filename, as_attachment=True)


# given selected checkboxes
# return motes and attributes
def get_sensors(selected):

    sensors = []

    for checkbox in selected:
        mote = str(checkbox[2:checkbox.index(",")-1])
        attribute = str(checkbox[checkbox.index(",")+3:-2])
        sensors.append([mote, attribute])

    return sensors


# given a list of selected checkboxes, start date, end date, and data
# flash appropriate messages on webpage
def flash_msgs(selected, date_start, date_end, data):

    if len(selected) == 0:
        flash("***Please choose at least one sensor***")
    if date_start == "":
        flash("***Please choose a start date***")
    if date_end == "":
        flash("***Please choose an end date***")
    if data == []:
        flash("***There is no data available for this time range " + str(date_start) + " to " + str(date_end) + "***")


## given a list of selected checkboxes, start date, end date, and data
## return a file and filename
def create_file(selected, date_start, date_end, data):
    ## This creates a filename specific to time range
    filename = "data" + date_start + "_to_" + date_end + ".txt"

    ## This writes data (this is a list) to file
    strIO = StringIO.StringIO()
    strIO.write("Start: " + date_start + "\n")
    strIO.write("End: " + date_end + "\n")
    strIO.write("Motes Selected: \n")

    for mote in selected:
        strIO.write(str(mote) + "\n")

    # This formats the data in the file; see format_download.py
    lengths = string_lengths(data)

    strIO.write(format_header(lengths))
    strIO.write(format_data(data, lengths))
    strIO.write(format_footer(lengths))

    strIO.seek(0)

    ## This clears the session of the variables
    session.pop('date_start', None)
    session.pop('date_end', None)

    return strIO, filename