# This file contains methods to format the data in the download file.


# given data
# returns a list stating the max length of each value in order
# timestamp, tag, attribute, value
def string_lengths(data):
    timestamp_length = 0
    tag_length = 0
    attribute_length = 0
    value_length = 0

    timestamps = []
    tags = [len("mote_tag")]
    attributes = [len("attribute")]
    values = [len("value")]

    for item in data:
        timestamps.append(len(str(item["timestamp"])))
        tags.append(len(str(item["mote_tag"])))
        attributes.append(len(str(item["attribute"])))
        values.append(len(str(item["value"])))

    timestamp_length = max(timestamps)
    tag_length = max(tags)
    attribute_length = max(attributes)
    value_length = max(values)

    return [timestamp_length, tag_length, attribute_length, value_length]


# given a list of lengths
# returns the top 3 lines of the table
def format_header(lengths):
    timestamp_length = lengths[0]
    tag_length = lengths[1]
    attribute_length = lengths[2]
    value_length = lengths[3]

    header1 = ("\n+" + "-" * (timestamp_length + 2) +
               "+" + "-" * (tag_length + 2) +
               "+" + "-" * (attribute_length + 2) +
               "+" + "-" * (value_length + 2) + "+")

    header2 = ("\n| " + "timestamp".ljust(timestamp_length + 1, " ") +
               "| " + "mote_tag".ljust(tag_length + 1, " ") +
               "| " + "attribute".ljust(attribute_length + 1, " ") +
               "| " + "value".ljust(value_length + 1, " ") + "|")

    return (header1 + header2 + header1 + "\n")


# given data and a list of lengths
# returns the middle of the table
def format_data(data, lengths):
    table = ""
    attribute_length = lengths[2]
    value_length = lengths[3]

    for item in data:
        table = table + ("| " + str(item["timestamp"]) +
                         " | " + str(item["mote_tag"]) +
                         " | " + str(item["attribute"].ljust(attribute_length, " ")) +
                         " | " + str(item["value"]).rjust(value_length, " ") + " |\n")

    return table


# given a list of lengths
# returns the bottom line of the table
def format_footer(lengths):
    timestamp_length = lengths[0]
    tag_length = lengths[1]
    attribute_length = lengths[2]
    value_length = lengths[3]

    footer = ("+" + "-" * (timestamp_length + 2) +
              "+" + "-" * (tag_length + 2) +
              "+" + "-" * (attribute_length + 2) +
              "+" + "-" * (value_length + 2) + "+")

    return footer
