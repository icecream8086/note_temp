import os

def remove_text_from_filenames(directory, text_to_remove):
    for filename in os.listdir(directory):
        if text_to_remove in filename:
            new_filename = filename.replace(text_to_remove, '')
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
            print(f'Renamed: {filename} -> {new_filename}')

if __name__ == "__main__":
    directory = r"C:\\Users\\zzbsn\\source\\repos\\VsCode\\note_temp\\output"
    text_to_remove = "【公众号：研料库，料最全】"
    remove_text_from_filenames(directory, text_to_remove)
