import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os

# Путь к файлу для хранения избранных пользователей
FAVORITES_FILE = "favorites.json"

class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.root.geometry("600x500")

        # Загрузка избранных пользователей
        self.favorites = self.load_favorites()

        self.setup_ui()

    def setup_ui(self):
        # Поле ввода для поиска
        tk.Label(self.root, text="Введите имя пользователя GitHub:").pack(pady=5)
        self.search_entry = tk.Entry(self.root, width=50)
        self.search_entry.pack(pady=5)

        # Кнопка поиска
        search_btn = tk.Button(self.root, text="Найти", command=self.search_user)
        search_btn.pack(pady=5)

        # Список результатов поиска
        self.results_list = tk.Listbox(self.root, height=10, width=70)
        self.results_list.pack(pady=10)

        # Кнопка добавления в избранное
        add_favorite_btn = tk.Button(self.root, text="Добавить в избранное",
                                    command=self.add_to_favorites)
        add_favorite_btn.pack(pady=5)

        # Список избранных пользователей
        tk.Label(self.root, text="Избранные пользователи:").pack(pady=5)
        self.favorites_list = tk.Listbox(self.root, height=8, width=70)
        self.favorites_list.pack(pady=10)

        # Обновление списка избранных
        self.update_favorites_list()

    def search_user(self):
        username = self.search_entry.get().strip()
        if not username:
            messagebox.showerror("Ошибка", "Поле поиска не должно быть пустым!")
            return

        try:
            response = requests.get(f"https://api.github.com/users/{username}")
            if response.status_code == 200:
                user_data = response.json()
                self.display_user(user_data)
            else:
                messagebox.showerror("Ошибка", f"Пользователь не найден (код: {response.status_code})")
        except requests.RequestException as e:
            messagebox.showerror("Ошибка сети", f"Не удалось подключиться к API: {e}")

    def display_user(self, user_data):
        self.results_list.delete(0, tk.END)
        info = f"{user_data['login']} - {user_data.get('name', 'Нет имени')} - {user_data.get('public_repos', 0)} репозиториев"
        self.results_list.insert(tk.END, info)

    def add_to_favorites(self):
        selection = self.results_list.curselection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите пользователя из списка результатов!")
            return

        user_info = self.results_list.get(selection[0])
        username = user_info.split(" - ")[0]

        if username not in self.favorites:
            self.favorites.append(username)
            self.save_favorites()
            self.update_favorites_list()
            messagebox.showinfo("Успех", f"{username} добавлен в избранное!")
        else:
            messagebox.showinfo("Информация", f"{username} уже в избранном!")

    def load_favorites(self):
        if os.path.exists(FAVORITES_FILE):
            with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_favorites(self):
        with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.favorites, f, ensure_ascii=False, indent=2)

    def update_favorites_list(self):
        self.favorites_list.delete(0, tk.END)
        for user in self.favorites:
            self.favorites_list.insert(tk.END, user)

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubUserFinder(root)
    root.mainloop()
