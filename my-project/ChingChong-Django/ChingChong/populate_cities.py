import os
import django
import sys

# Добавляем путь к проекту в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChingChong.settings')
django.setup()

from main.utils import import_cities

def main():
    # Путь к CSV файлу
    csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'city.csv')
    
    # Импортируем города
    import_cities(csv_file_path)
    print("Импорт городов завершен успешно!")

if __name__ == '__main__':
    main()
