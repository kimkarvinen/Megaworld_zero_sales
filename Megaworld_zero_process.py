import os
import shutil
from datetime import datetime, timedelta

def add_one_day_to_date(date_str):
    if len(date_str) == 10:
        line = date_str[:2]  # Extract line number
        date_part = date_str[2:]  # Extract date part
        date_format = "%m%d%Y"
        date = datetime.strptime(date_part, date_format)
        new_date = date + timedelta(days=1)
        new_date_str = new_date.strftime(date_format)
        return f"{line}{new_date_str}"
    else:
        return "Date format not recognized"

def copy_contents(source_file, dest_file, lines=None, modify_d=False):
    with open(source_file, 'r') as f_src, open(dest_file, 'w') as f_dest:
        if lines is not None:
            for idx, line in enumerate(f_src):
                if idx >= lines:
                    break
                f_dest.write(line)
        elif modify_d:
            for line in f_src:
                parts = line.split(',')
                if len(parts) > 2:
                    parts[2] = '0.00'
                    line = ','.join(parts)
                f_dest.write(line + '\n')  # Insert newline after each line
        else:
            shutil.copyfileobj(f_src, f_dest)

def move_files():
    bugs_folder = "megaworld_bugs"
    sent_folder = "megaworld_sent"
    dest_folder = "D:/megaworld"  # Destination directory
    
    if not os.path.exists(bugs_folder) or not os.path.exists(sent_folder):
        print(f"Error: {bugs_folder} or {sent_folder} folder not found.")
        return
    
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # Create destination directory if it doesn't exist
    
    print("Copying and modifying files from megaworld_sent to megaworld_bugs...")

    for filename in os.listdir(sent_folder):
        sent_filename = os.path.join(sent_folder, filename)
        first_letter = filename[0].lower()
        for bugs_filename in os.listdir(bugs_folder):
            bugs_first_letter = bugs_filename[0].lower()
            if bugs_first_letter == first_letter:
                bugs_path = os.path.join(bugs_folder, bugs_filename)
                if first_letter == 's':
                    with open(sent_filename, 'r') as f_sent, open(bugs_path, 'w') as f_bugs:
                        lines = f_sent.readlines()
                        if len(lines) >= 3:
                            date_line = lines[2].strip()
                            new_date_line = add_one_day_to_date(date_line)
                            lines[2] = new_date_line + '\n'
                            if len(lines) >= 5:
                                line_5 = lines[4].strip()
                                if len(line_5) >= 3:
                                    line_4 = '04' + line_5[2:]
                                    lines[3] = line_4 + '\n'
                                    f_bugs.writelines(lines[:5])
                                else:
                                    print(f"Warning: Line 5 in '{filename}' does not have enough characters. Skipping.")
                            else:
                                print(f"Error: Not enough lines in '{filename}' to perform the operation.")
                            # Append additional lines
                            additional_lines = [
                                '06000',
                                '07000',
                                '08000',
                                '09000',
                                '10000',
                                '11000',
                                '12000',
                                '13000',
                                '14000',
                                '15000',
                                '16000',
                                '17000',
                                '180',
                                '190',
                                '200',
                                '2101',
                                '22000'
                            ]
                            f_bugs.writelines([line + '\n' for line in additional_lines])
                            print(f"Appended additional lines to '{filename}'.")
                        else:
                            print(f"Error: Not enough lines in '{filename}' to perform the operation.")
                    shutil.move(bugs_path, os.path.join(dest_folder, bugs_filename))  # Move processed file
                elif first_letter == 'h':
                    with open(sent_filename, 'r') as f_sent, open(bugs_path, 'w') as f_bugs:
                        lines = f_sent.readlines()
                        if len(lines) >= 3:
                            date_line = lines[2].strip()
                            new_date_line = add_one_day_to_date(date_line)
                            lines[2] = new_date_line + '\n'
                            f_bugs.writelines(lines[:3])
                            # Append additional lines
                            additional_lines = [
                                '04',  # Additional line with modified day value
                                '05',
                                '06',
                                '07',
                                '08',
                                '09',
                                '10'
                            ]
                            f_bugs.writelines([line + '\n' for line in additional_lines])
                            print(f"Appended additional lines to '{filename}'.")
                        else:
                            print(f"Error: Not enough lines in '{filename}' to perform the operation.")
                    shutil.move(bugs_path, os.path.join(dest_folder, bugs_filename))  # Move processed file
                elif first_letter == 'd':
                    copy_contents(sent_filename, bugs_path, modify_d=True)
                    shutil.move(bugs_path, os.path.join(dest_folder, bugs_filename))  # Move processed file
                    print(f"Processed '{filename}' for modifying values after 2nd comma.")
                else:
                    copy_contents(sent_filename, bugs_path)
                    shutil.move(bugs_path, os.path.join(dest_folder, bugs_filename))  # Move processed file
                    print(f"Processed '{filename}' by direct copy.")

    print("Files copied, modified, and moved to D:/megaworld.")

if __name__ == "__main__":
    move_files()
