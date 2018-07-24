from tkinter import *

import requests
import json


class SearchResult:
    def __init__(self, json):
        self.description = json["description"]
        self.monthly = json["monthly"]
        self.month = json["month"]
        self.year = json["year"]
        self.query = json["query"]
        self.path = json["path"]
        self.results = json["results"]


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.entry_list = {}
        self.search_type = "exact"
        self.box = None
        self.init_window()

    def init_window(self):
        self.master.title("F@H stats")
        self.pack(fill=BOTH, expand=1)

        entries = ["name", "passkey", "team", "month", "year"]

        counter = 0
        for entry in entries:
            lbl = Label(self, text=entry + ": ")
            lbl.place(x=5, y=5 + 25 * counter)
            ent = Entry(self)
            ent.place(x=75, y=5 + 25 * counter)
            self.entry_list[entry] = ent
            counter += 1
        var = StringVar()
        rad = Radiobutton(self, text="Search Exact", variable=var, value="exact", command=lambda: self.select(var))
        rad.select()
        rad.place(x=5, y=5 + 25 * counter)
        counter += 1

        rad = Radiobutton(self, text="Search Like", variable=var, value="like", command=lambda: self.select(var))
        rad.place(x=5, y=5 + 25 * counter)
        rad.deselect()
        counter += 1

        rad = Radiobutton(self, text="Search Prefix", variable=var, value="prefix", command=lambda: self.select(var))
        rad.place(x=5, y=5 + 25 * counter)
        rad.deselect()
        counter += 1

        button = Button(self, text="Search", command=self.search)
        button.place(x=5, y=5 + 25 * counter)
        counter += 1
        scroll = Scrollbar(self)
        scroll.place(x=720 - 17, y=250, height=25 * 16)

        self.box = Listbox(self, yscrollcommand=scroll.set, width=115, height=25, selectmode=EXTENDED)
        self.box.place(x=5, y=250)

        scroll.config(command=self.box.yview)

    def select(self, search_type):
        self.search_type = search_type.get()

    def search(self):
        name = self.entry_list["name"].get()
        search_type = self.search_type
        passkey = self.entry_list["passkey"].get()
        team = self.entry_list["team"].get()
        month = self.entry_list["month"].get()
        year = self.entry_list["year"].get()

        if team and not team.isdigit():
            self.box.delete(0, END)
            self.box.insert(END, "Searching via team requires their the teamID, not their name!")
            return

        url = get_url(name, search_type, passkey, team, month, year)
        try:
            req = requests.get(url).text
            results = SearchResult(json.loads(req))
            self.box.delete(0, END)
            if not results.results:
                self.box.insert(END, "No data found.")
            for idx, result in enumerate(results.results):
                self.box.insert(END, "{}) Name: {},     WUs: {},     Rank: {},     Credit: {},     Team: {},     Id: {}".format(idx + 1, result["name"], result["wus"], result["rank"], result["credit"], result["team"], result["id"]))
        except Exception as x:
            self.box.insert(END, "Unable to connect to the server. Is your internet connected?")
            self.box.insert(END, x)


def main():
    root = Tk()
    root.geometry("720x720")
    Window(root)
    root.mainloop()


def get_url(name="", search_type="prefix", passkey="", team="", month="", year=""):
    return "https://stats.foldingathome.org/api/donors?name={}&search_type={}&passkey={}&team={}&month={}&year={}".format(name, search_type, passkey, team, month, year)


if __name__ == '__main__':
    main()
