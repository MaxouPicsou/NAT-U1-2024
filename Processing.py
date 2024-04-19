from datetime import datetime

EVENT_TIMESTAMP_FILENAME = "event_file.txt"
EVENT_ACTION_FILENAME = "action_file.csv"
FIRST_ACTION_TIME = 14

first_action_find = False
first_action_timestamp = 0

with open(EVENT_TIMESTAMP_FILENAME, 'r') as file_to_read:
    with open(EVENT_ACTION_FILENAME, 'w') as file_to_write:
        file_to_write.write(
            "Action,Type,Time(s),Time (GMT+0000),Time (GMT+0200),Video time (s),Video time (hh:mm:ss)\n")
        for line in file_to_read:
            if (("code 272" in line) or ("code 273" in line) or ("code 274" in line) or ("code 28" in line) or ("code 96" in line)) and "val 00" in line:
                timestamp_s = line.split(" ")[2].replace(",", "")
                if "code 272" in line:
                    action = "Left Click"
                elif "code 273" in line:
                    action = "Right Click"
                elif "code 274" in line:
                    action = "Wheel Click"
                elif "code 28" in line or "code 96" in line:
                    action = "ENTER Key"

                if not first_action_find:
                    first_action_timestamp = float(timestamp_s)
                    first_action_find = True

                hour_GMT_0 = datetime.utcfromtimestamp(float(timestamp_s)).strftime("%H:%M:%S")
                hour_GMT_2 = datetime.utcfromtimestamp(float(timestamp_s) + 3600 * 2).strftime("%H:%M:%S")
                video_time_s = int(FIRST_ACTION_TIME + float(timestamp_s) - first_action_timestamp)
                video_time_hhmmss = datetime.utcfromtimestamp(float(video_time_s)).strftime("%H:%M:%S")
                file_to_write.write("," + action + "," + timestamp_s + "," + hour_GMT_0 + "," + hour_GMT_2 + "," +
                                    str(video_time_s) + "," + video_time_hhmmss + "\n")
