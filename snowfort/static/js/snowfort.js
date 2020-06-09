/**
 * Timer Class
 * That will be used for enabling and disabling an interval.
 * http://stackoverflow.com/questions/3249491/what-is-a-more-elegant-way-of-toggling-a-javascript-timer
 *
 * @param {ms} The milliseconds delay for firing an event.
 * @param {func} The function to perform on each interval.
 */
function Timer(ms, func) {
  this.f = func;
  this.timeout = ms;
  this.current = 0;

  this.enable = function () {
    this.current = setInterval(this.f, this.timeout);
  };

  this.disable = function () {
    clearInterval(this.current); this.current = 0;
  };

  this.toggle = function () {
    if (this.current > 0) {
      this.disable();
    } else {
      this.enable();
    }
  };
};

/**
 * Graph Class
 *
 * @param {placeholder} The ID of the placeholder for the graph. Without the #.
 * @param {url} The URL to fetch data for the graph.
 * @param {legend} The ID of the legend for the graph. Without the #.
 */
function Graph(placeholder, legend, baseUrl, stationId, attribute) {
  this.placeholder = "#" + placeholder;
  this.legend = "#" + legend;
  this.toggle = {};

  /* Keeping track of constructing the URL */
  this.baseUrl = baseUrl;
  this.stationId = stationId;
  this.attribute = attribute;
  this.lastStart = undefined;
  this.lastEnd = undefined;

  this.url = baseUrl + "/" + stationId + "/" + attribute;

  var obj = this;
  // this.timer = new Timer(60000, function () { obj.fetchData(); });
  this.timer = new Timer(1000, function () { obj.fetchData(); });

  this.data = [];

  function showTooltip (x, y, contents) {
    $("<div id=\"tooltip\" class=\"graph-tooltip\">" + contents + "</div>").css({
      top: y + 5,
      left: x - 10,
    }).appendTo("body").fadeIn(200);
  }

  /* Bind event for hovering over a plot point and showing the tooltip with data. */
  $(this.placeholder).bind("plothover", function (event, pos, item) {
    if (item) {
      document.body.style.cursor = "pointer";
      if (previousPoint != item.dataIndex) {
        previousPoint = item.dataIndex;

        $("#tooltip").remove();
        var x = item.datapoint[0].toFixed(2),
            y = item.datapoint[1].toFixed(2);

        var date = new Date(parseInt(x));
        var show_date = new Date(date.getUTCFullYear(),
                                 date.getUTCMonth(),
                                 date.getUTCDate(),
                                 date.getUTCHours(),
                                 date.getUTCMinutes(),
                                 date.getUTCSeconds());
        /* Get browser offset for timezone. */
        show_date.setTime(show_date.valueOf() - 60000 * show_date.getTimezoneOffset());
        showTooltip(item.pageX, item.pageY + 20,
                    "<strong>" + y + "</strong><br />" + item.series.label + "<br />" + show_date.toLocaleString());
      }
    } else {
      $("#tooltip").remove();
      previousPoint = null;
      document.body.style.cursor = "auto";
    }
  });

  /* Time dragger. */
  var dragger = document.getElementById(placeholder);
  dragger.onmousedown = function (event) {
    console.log("mouse down");
    obj.mouseDown(event);
    event.preventDefault();
  }
};

/**
 * Mouse Down to trigger the movement. Only works if dates are given. No
 * dates given then won't be able to shift.
 *
 * @param {event} The event handler.
 */
Graph.prototype.mouseDown = function (event) {
  if (this.lastStart === undefined || this.lastEnd === undefined) { return; }
  this.down = true;

  var obj = this;
  this.oldUpHandler = document.body.onmouseup;
  document.body.onmouseup = function(event) { obj.mouseUp(event); }
  document.body.style.cursor = "w-resize";
  this.oldMoveHandler = document.body.onmousemove;
  document.body.onmousemove = function(event) { obj.moveMouse(event); }

  /* Get initial click coordinates. */
  this.startX = event.clientX;
  this.tempStart = this.lastStart;
  this.tempEnd = this.lastEnd;
};

/**
 * Mouse Move which will adjust the time depending on the direction of movement.
 *
 * @param {event} The event handler.
 */
Graph.prototype.moveMouse = function (event) {
  if (this.lastStart === undefined || this.lastEnd === undefined) { return; }
  if (!this.down) { return; }
  var dx = event.clientX - this.startX;
  console.log(dx);
  this.tempStart = this.lastStart + 10*dx;
  this.tempEnd = this.lastEnd + 10*dx;
  var url = [this.baseUrl, this.stationId, this.attribute, this.tempStart, this.tempEnd].join("/");

  // Update URL and old start/end
  this.updateQuery(url);
};

/**
 * Mouse Up Event to set the new start and end dates.
 *
 * @param {event} The event handler.
 */
Graph.prototype.mouseUp = function (event) {
  this.down = false;
  document.body.onmouseup = this.oldUpHandler;
  document.body.onmousemove = this.oldMoveHandler;
  document.body.style.cursor = "auto";
  this.lastStart = this.tempStart;
  this.lastEnd = this.tempEnd;
};


/**
 * The main fetching of data function. This will go to the endpoint retrieve the JSON data for the graph and
 * plot or update the plot. Uses ajax call.
 */
Graph.prototype.fetchData = function () {
  var obj = this;

  function labeler (label, series) {
    return "<a href=\"#\" id=\"toggle-" + series.idx + "\" class=\"btn btn-default btn-xs\">" + label + "</a>";
  };

  function onDataReceived (series) {
    obj.data = series.data;
    if (obj.data.length == 0) {
      var n = noty({layout: 'center', type: 'warning', text: '<strong>Warning</strong><br />No data in query, try a different query.', timeout: 3600});
    }
    obj.plot = $.plot(obj.placeholder, obj.data,
      { series: { lines: { show: true },
                  points: { show: true } },
          grid:   { hoverable: true },
         xaxis: { mode: "time",
		  font: {size: 20},
                  timeformat: "%m/%d %H:%M",
                  twelveHourClock: true,
                  timezone: "browser" },
        legend: { show: true,
                  noColumns: 10,
                  container: obj.legend,
                  labelFormatter: labeler }
      }
    );

    /* If we've had any toggles done then we need to persist them. */
    obj.setToggles(obj.toggle);

    /* Set up the onclick events for the legend. */
    $.each(obj.data, function (key, set) {
      var button = document.getElementById("toggle-" + set.idx);
      button.onclick = function (event) {
        obj.togglePlot(set.idx);
        event.preventDefault();
      }
    });

  }

  /* AJAX call to get JSON data from the endpoint. */
  $.ajax({
    url: this.url,
    type: "GET",
    dataType: "json",
    success: onDataReceived
  });
};

/**
 * Updates the current endpoint being used for the graph.
 *
 * @param {url} The endpoint to query for data that is being updated.
 */
Graph.prototype.updateQuery = function (url) {
  this.url = url;
  this.fetchData();
};

/**
 * Renders the plot for the first time.
 */
Graph.prototype.render = function () {
  var obj = this;
  this.plot = $.plot(obj.placeholder, this.data);
  this.fetchData();
};

/**
 * Toggle the plot point. This function is utilized to turn on and off series.
 *
 * @param {seriesIndex} The index of the series to toggle on and off. MUST match the idx given in data.
 */
Graph.prototype.togglePlot = function (seriesIndex) {
  var data = this.plot.getData();
  data[seriesIndex].lines.show = !data[seriesIndex].lines.show;
  data[seriesIndex].points.show = !data[seriesIndex].points.show;
  this.toggle[seriesIndex] = data[seriesIndex].lines.show;
  this.plot.setData(data);
  this.plot.draw();
};

/**
 * Sets the toggle set for the graph. Thus if an item is in the hash then it'll contain a value of the toggle
 * value that should be set to when displaying. This will regenerate the plot afterward as well.
 *
 * @param {hash} The hash of what series index toggle values are.
 */
Graph.prototype.setToggles = function (hash) {
  var data = this.plot.getData();
  for (var key in hash) {
    data[key].lines.show = hash[key];
    data[key].points.show = hash[key];
  }
  this.plot.setData(data);
  this.plot.draw();
};

/**
 * Set up real time button that will alternate the text and class name based
 * off Bootstrap styling.
 *
 * @param {buttonId} The button_id that you want to enable as real-time.
 */
Graph.prototype.setUpRealTime = function (buttonId) {
  var realtime = document.getElementById(buttonId);
  realtime.innerHTML = "Enable Real-Time";
  realtime.className = "btn btn-success";

  var obj = this;
  realtime.onclick = function (event) {
    obj.timer.toggle();
    if (obj.timer.current > 0) {
      this.innerHTML = "Disable Real-Time";
      this.className = "btn btn-danger";
    } else {
      this.innerHTML = "Enable Real-Time";
      this.className = "btn btn-success";
    }
  };
};

/**
 * Set up datetime pickers by providing the form fields ids and the button to
 * cause the query to execute.
 * This requires that snowfort.js come AFTER the jquery.datetimepicker.js
 * which in general it will for how we structure our scripts. All plugins first
 * then our scripts.
 *
 * @param {startId} The start id input field. Without the #.
 * @param {endId} The end id input field. Without the #.
 * @param {goId} The button id for the query button. Without the #.
 * @param {clearId} The button id for the clear button. Without the #.
 */
Graph.prototype.setUpDatePicker = function (startId, endId, goId, clearId) {
  var jqStartId = "#" + startId; // Used with jQuery
  var jqEndId = "#" + endId; // Used with jQuery

  /* Create date time picker for start */
  $(jqStartId).datetimepicker({
    step: 30,
    onShow: function (event) {
      this.setOptions({
        maxDate: $(jqEndId).val() ? $(jqEndId).val().substring(0, 10) : false
      })
    }
  });

  $(jqEndId).datetimepicker({
    step: 30,
    onShow: function (event) {
      this.setOptions({
        minDate: $(jqStartId).val() ? $(jqStartId).val().substring(0, 10) : false
      })
    }
  });

  /* Set up the events for time changes */
  var go = document.getElementById(goId);
  var obj = this;
  go.onclick = function (event) {
    var start = getUTCEpochSeconds(startId, 0);
    var end = getUTCEpochSeconds(endId, 253402246297); // Date: 12/31/9999

    /* Construct the URL */
    var url = [obj.baseUrl, obj.stationId, obj.attribute, start, end].join("/");

    // Update URL and old start/end
    obj.updateQuery(url);
    obj.lastStart = start;
    obj.lastEnd = end;
  };

  var clear = document.getElementById(clearId);
  clear.onclick = function (event) {
    document.getElementById(startId).value = "";
    document.getElementById(endId).value = "";

    var url = [obj.baseUrl, obj.stationId, obj.attribute].join("/");
    obj.updateQuery(url);
    obj.lastStart = undefined;
    obj.lastEnd = undefined;
  };
};

/**
 * Update the attribute setting for the graph.
 * This is particular to the implementation.
 *
 * @param {newAttr} The new attribute that will be used in the URL.
 */
Graph.prototype.updateAttribute = function (newAttr) {
  this.attribute = newAttr;
  var args = [this.baseUrl, this.stationId, this.attribute];
  if (this.lastStart !== undefined && this.lastEnd !== undefined) {
    args.push.apply(args, [this.lastStart, this.lastEnd]);
  }
  var url = args.join("/");
  this.updateQuery(url);
};

/**
 * Gets the Date Time string from an input field and converts to UTC Epoch
 * Seconds. The Date Time string should be of format YYYY/MM/DD HH:MM.
 *
 * @param {inputId} The input id holding the string to convert.
 * @param {clip} The default value to return if empty.
 */
function getUTCEpochSeconds (inputId, clip) {
  var tstring = document.getElementById(inputId).value;
  if (tstring.length === 0) { return clip; }

  /* The Date Time Picker guarantees valid formatted data. */
  var date = new Date(tstring);
  date.setTime(date.valueOf() + 60000 * date.getTimezoneOffset());

  var epoch = Date.UTC(date.getFullYear(), date.getMonth(), date.getDate(),
                       date.getHours(), date.getMinutes(), date.getSeconds());
  return epoch / 1000;
};
