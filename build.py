#!/usr/bin/env python3
import os
import platform
import subprocess
import shutil

def main():
    print("Видео Анализатор - Скрипт сборки")
    print("--------------------------------")
    
    # Очистка предыдущих сборок
    if os.path.exists("dist"):
        print("Удаление предыдущих сборок...")
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # Определение текущей платформы
    current_os = platform.system()
    print(f"Обнаружена платформа: {current_os}")
    
    # Установка PyInstaller, если необходимо
    print("Установка PyInstaller...")
    subprocess.run(["pip", "install", "pyinstaller"], check=True)
    
    # Установка зависимостей
    print("Установка зависимостей...")
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
    
    # Сборка для текущей платформы
    print(f"Сборка для {current_os}...")
    
    if current_os == "Windows":
        subprocess.run(["pyinstaller", "--onefile", "--name=video_analyzer", "main.py"], check=True)
        output_file = "dist/video_analyzer.exe"
    elif current_os == "Darwin":  # macOS
        subprocess.run(["pyinstaller", "--onefile", "--name=video_analyzer", "main.py"], check=True)
        output_file = "dist/video_analyzer"
    elif current_os == "Linux":
        subprocess.run(["pyinstaller", "--onefile", "--name=video_analyzer", "main.py"], check=True)
        output_file = "dist/video_analyzer"
    else:
        print(f"Неподдерживаемая платформа: {current_os}")
        return
    
    if os.path.exists(output_file):
        print(f"Сборка успешно завершена! Исполняемый файл: {output_file}")
        size_mb = os.path.getsize(output_file) / (1024 * 1024)
        print(f"Размер файла: {size_mb:.2f} МБ")
        
        # Инструкции по использованию
        print("\nКак использовать:")
        print(f"{output_file} video.mp4 --mode shake --output results.json")
    else:
        print("Сборка не удалась!")

if __name__ == "__main__":
    main() 