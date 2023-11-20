import os
import shutil
import sys




def sort_files(folder_path):
    # Перевірка, чи існує задана папка
    if not os.path.exists(folder_path):
        print(f"Папка {folder_path} не існує.")
        return
    

    image_files = []
    video_files = []
    document_files = []
    audio_files = []
    archive_files = []
    other_files = []

    # множини щоб значення не повторювались
    known_extensions = set()
    unknown_extensions = set()


    # прописать путь к новым папкам в переменных
    image_folder = os.path.join(folder_path, 'images')
    video_folder = os.path.join(folder_path, 'videos')
    document_folder = os.path.join(folder_path, 'documents')
    audio_folder = os.path.join(folder_path, 'audio')
    archives_folder = os.path.join(folder_path, 'archives')
    other_folder = os.path.join(folder_path, 'other')

    # передираем пути, если нет нужной папки она создаётся
    for folder in [image_folder, video_folder, document_folder, audio_folder, archives_folder, other_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    exclude = [image_folder, video_folder, document_folder, audio_folder, archives_folder, other_folder]

    def walk(folder_path):
        for (root, dirs, files) in os.walk(folder_path):
            # если эта путь папки совпадает с путями папок которые мы создали игнорируем
            if any(exclude_f in root for exclude_f in exclude):
                continue
            else:
                # если не совпадает заходим в неё и перебираем все эл в ней
                for filename in files:
                    file_path = os.path.join(root, filename)

                    # определяем суффикс файла деля его по точке
                    _, file_extension = os.path.splitext(filename)
                    file_extension = file_extension.lower()

                 # сортируем по окончаниям в созданные папки 
                    if file_extension in ('.jpeg', '.png', '.jpg', '.svg'):
                        shutil.move(file_path, os.path.join(image_folder, filename))

                    elif file_extension in ('.avi', '.mp4', '.mov', '.mkv'):
                        shutil.move(file_path, os.path.join(video_folder, filename))

                    elif file_extension in ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'):
                        shutil.move(file_path, os.path.join(document_folder, filename))

                    elif file_extension in ('.mp3', '.ogg', '.wav', '.amr'):
                        shutil.move(file_path, os.path.join(audio_folder, filename))

                    elif file_extension in ('.zip', '.gz', '.tar'):
                        # архив распаковать в новую папку по названию архива
                        # прописываем полный адрес куда распаковать(адрес папки, название архива(файла) без расширения)
                        archive_folder = os.path.join(archives_folder, os.path.splitext(filename)[0])
                        try:
                            shutil.unpack_archive(file_path, archive_folder)
                        except shutil.ReadError:
                            continue

                        # переместить архив в папку к архивам
                        shutil.move(file_path, os.path.join(archives_folder, filename))
                        
                    else:
                        shutil.move(file_path, os.path.join(other_folder, filename))




                
    def remove_empty_folders(folder_path):
        for (root, dirs, files) in os.walk(folder_path, topdown=False):
            # если эта путь папки совпадает с путями папок которые мы создали игнорируем
            if any(exclude_f in root for exclude_f in exclude):
                continue
            # удаляем пустые и игнорируем исходную папку
            else:
                if not files and root != folder_path:
                    os.rmdir(root)

    def normalize(folder_path):
        translit_dict = {
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Ґ': 'G',
    'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Є': 'IE', 'Ж': 'ZH', 'З': 'Z',
    'И': 'I', 'І': 'I', 'Ї': 'I', 'Й': 'I', 'К': 'K',
    'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P',
    'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F',
    'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH',
    'Ь': '', 'Ъ': '', 'Ю': 'IU', 'Я': 'IA', 'Э': 'e',
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'ґ': 'g',
    'д': 'd', 'е': 'e', 'ё': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
    'и': 'i', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k',
    'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
    'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
    'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
    'ь': '', 'ъ': '', 'ю': 'iu', 'я': 'ia', 'э': 'e',
}
        for root, _, files in os.walk(folder_path):
            for file in files:
                # разделяем название от расширения
                name, extension = os.path.splitext(file)
                # нормализируем имя, если латинские буквы или цифры вставляем без изменений, кирилицу - транслителируем, остальное меняем на _
                normalized_name = ''.join(translit_dict.get(c, '_') if not (65 <= ord(c) <= 90 or 97 <= ord(c) <= 122 or 48 <= ord(c) <= 57) else c for c in name)
                # соединить название и расширение
                new_file_name = normalized_name + extension
                # прописать пути
                old_file_path = os.path.join(root, file)
                new_file_path = os.path.join(root, new_file_name)
                # переименовать
                os.rename(old_file_path, new_file_path)


    def stat(folder_path):
        for (root, dirs, files) in os.walk(folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)

                _, file_extension = os.path.splitext(filename)
                file_extension = file_extension.lower()

                if file_extension in ('.jpeg', '.png', '.jpg', '.svg'):
                    image_files.append(filename)
                    if file_extension: 
                        known_extensions.add(file_extension)

                elif file_extension in ('.avi', '.mp4', '.mov', '.mkv'):
                    video_files.append(filename)
                    if file_extension: 
                        known_extensions.add(file_extension)

                elif file_extension in ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'):
                    document_files.append(filename)
                    if file_extension: 
                        known_extensions.add(file_extension)

                elif file_extension in ('.mp3', '.ogg', '.wav', '.amr'):
                    audio_files.append(filename)
                    if file_extension: 
                        known_extensions.add(file_extension)

                elif file_extension in ('.zip', '.gz', '.tar'):
                    archive_files.append(filename)
                    if file_extension: 
                        known_extensions.add(file_extension)
                        
                else:
                    other_files.append(filename)
                    if file_extension:  # Додаємо перевірку на наявність розширення перед додаванням до множини
                        unknown_extensions.add(file_extension)




    normalize(folder_path)
    walk(folder_path)
    remove_empty_folders(folder_path)
    stat(folder_path)



    return {
        'images': image_files,
        'videos': video_files,
        'documents': document_files,
        'audio': audio_files,
        'archives': archive_files,
        'other': other_files,
        'KnownExtensions': known_extensions,
        'UnknownExtensions': unknown_extensions
    }

#проверяем правильно ли кол во аргументов ввели в консоль 
if __name__ == "__main__":
    # Перевірка наявності аргументів командного рядка
    if len(sys.argv) != 2:
        print("Введіть шлях до папки для сортування.")
    else:
        folder_to_sort = sys.argv[1]
        result = sort_files(folder_to_sort)

for category, files in result.items():
    print(f"{category}: {files}")
