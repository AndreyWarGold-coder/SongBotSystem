import random
import SL_Settings
import WW_String
import dropboxFN
import Viewers


class User:
    def __init__(self, name: str = "", id: str = ""):
        print(name, id)
        self.name: str = name
        self.id: str = id
        nameFile = str(name)+str(id)
        tmp = None
        if(nameFile in self.get_list_users()):
            tmp = SL_Settings.load_obj(nameFile, "users")
        else:
            tmp = {"songs": 0,
               "authors": 0,
               "skips": 0,
               "wins": 0,
               "loss": 0}
            SL_Settings.save_obj(tmp, nameFile, "users")
        self.songs = tmp["songs"]
        self.authors = tmp["authors"]
        self.skips = tmp["skips"]
        self.wins = tmp["wins"]
        self.loss = tmp["loss"]
        print("Have been created user", self.name, self.id)

    def get_list_users(self):
        list_users = dropboxFN.dropbox_list_files("users")
        tmp = []
        for i in list_users:
            tmp.append(i.split(".")[0])
        print(tmp)
        return tmp

    def save_parameters(self):
        tmp = {"songs": self.songs,
               "authors": self.authors,
               "skips": self.skips,
               "wins": self.wins,
               "loss": self.loss}
        SL_Settings.save_obj(tmp, self.name+self.id, "users")

class Music:
    def __init__(self, name: str, author: str, category: str = "",views = 0):
        self.name = name
        self.author = author
        self.category = category
        self.views = 0
        self.views = views

    def get_file(self):
        rand_index = random.randint(0, 2)
        file = dropboxFN.dropbox_download_file("music/"+self.author+"_"+self.name+"_"+str(rand_index)+".mp3")
        return file

    def get_views_in_text(self):
        print("IN:", self.views)
        tmp = ""
        list_tmp = []
        colvo = self.views
        list_razr = list(str(colvo))
        tt = 0
        for i in range(len(list_razr)):
            y = (len(list_razr)-1)-i
            tt+=1
            if(tt != 3):
                list_tmp.append(list_razr[y])
            else:
                tt = 0
                list_tmp.append(","+list_razr[y])
        for y in range(len(list_tmp)):
            i = (len(list_tmp)-1)-y
            tmp+=list_tmp[i]
        if(tmp.startswith(",")):
            list_tmp = list(tmp)
            list_tmp.remove(",")
            tmp = ""
            for i in list_tmp:
                tmp+=i
        print("OUT:", tmp)
        return tmp

class CategoryController:
    def __init__(self, list_view):
        self.list_view = list_view

    def get_list_category(self):
        tmp = dropboxFN.dropbox_list_files("categorys")
        list_tmp = ["category_Random"]
        for i in tmp:
            list_tmp.append("category_"+i.split(".")[0])
        return list_tmp

    def get_list_music_by_category(self, category: str = "Random"):
        if(category != "Random"):
            return SL_Settings.load_obj(category, "categorys")
        else:
            tmp = dropboxFN.dropbox_list_files("music")
            list_tmp = []
            for i in tmp:
                if(i.endswith("_0.mp3")):
                    list_tmp.append(i.split("_0.mp3")[0])
            return list_tmp

    def get_music_by_category(self, category: str = "Random"):
        list_music = []
        list_music = self.get_list_music_by_category(category)
        print(list_music, len(list_music))
        b = len(list_music)-1
        index = random.randint(0, b)
        author_music = ""
        name_music = ""
        tmp = list_music[index].split("_")
        if(len(tmp) > 2):
            name_music = list_music[index].split("_")[-1].split(".mp3")[0]
            author_music = list_music[index].split("_"+name_music)[0]
        else:
            author_music = list_music[index].split("_")[0]
            name_music = list_music[index].split("_")[1].split(".mp3")[0]
        return Music(name_music, author_music, category, self.list_view[author_music+"_"+name_music])

    def add_category(self):
        raise Exception("None this method")


class Session:
    def __init__(self, chat_id: str, mode: str, messager: str, host: str):
        self.chat_id = chat_id
        self.mode = mode
        self.messager = messager
        self.host = host
        self.list_user: list[User] = []

    def get_id(self):
        return self.chat_id

    def isUser(self, name:str, id:str):
        for i in self.list_user:
            if(i.name == name and i.id == id):
                return True
        return False

    def get_user(self, name:str, id:str):
        for i in self.list_user:
            if(i.name == name and i.id == id):
                return i
        return None

    def add_user(self, name:str, id:str):
        if not self.isUser(name, id):
            self.list_user.append(User(name, id))

    def del_user(self, name:str, id:str):
        if self.isUser(name, id):
            self.list_user.remove(self.get_user(name, id))

    def start_message(self):
        pass

    def click_button(self, button: str = "", user_name: str = "None", user_id: str = "None"):
        pass

    def next_step(self, text: str = "", user_name: str = "None", user_id: str = "None"):
        pass

    def end(self):
        pass

class ReturnCommandObj:
    def __init__(self, text: str = None, buttons = None, replyText: str = None, file = None, isEnd = False):
        self.text = text
        self.buttons = buttons
        self.replyText = replyText
        self.file = file
        self.isEnd = isEnd

class UpDownSession(Session):
    def __init__(self, chat_id: str, mode: str, messager: str, host: str, category_controller: CategoryController):
        super().__init__(chat_id, mode, messager, host)
        self.category_controller = category_controller
        self.category = None
        self.music: Music = None
        self.last_music: Music = None
        self.max_rating = 0

    def next_step(self, text: str = "", user_name: str = "None", user_id: str = "None", isWin = True):
        if user_name != self.host:
            return None
        if isWin != True:
            return ReturnCommandObj("Нажаль, ви помилилися =( \nВаш рекорд прогнозів: " + str(self.max_rating), isEnd=True)
        if not self.isUser(user_name, user_id):
            self.add_user(user_name, user_id)
        user: User = self.get_user(user_name, user_id)
        if self.music == None:
            self.music = self.category_controller.get_music_by_category(self.category)
            if self.last_music == None:
                self.last_music = self.category_controller.get_music_by_category(self.category)
                return ReturnCommandObj("Минула пісня "+self.last_music.author+" - "+self.last_music.name+". \n👁‍🗨: " +str(self.last_music.get_views_in_text())+"\nВам надано 10 секунд пісні, спробуйте вгадати чи вона популярніша, чи менш популярніша від минулої", buttons=["_🔼", "_🔽"], file=self.music.get_file())
            else:
                return ReturnCommandObj("Минула пісня "+self.last_music.author+" - "+self.last_music.name+". \n👁‍🗨: " +str(self.last_music.get_views_in_text())+"\nВам надано 10 секунд пісні, спробуйте вгадати чи вона популярніша, чи менш популярніша від минулої",
                                        buttons=["_🔼", "_🔽"], file=self.music.get_file())

    def set_category(self, text: str, user_name: str = None, user_id: str = None):
        self.category = text
        return self.next_step(user_name=user_name, user_id=user_id)

    def click_button(self, button: str = "", user_name: str = "None", user_id: str = "None"):
        if user_name != self.host:
            return None
        if(button.startswith("category_")):
            return self.set_category(button.split("_")[1], user_name=user_name, user_id=user_id)
        elif(button == "🔼"):
            last_views = self.last_music.views
            now_views = self.music.views
            isWin = False
            if now_views >= last_views:
                self.max_rating += 1
                isWin = True
            self.last_music = self.music
            self.music = None
            return self.next_step(user_name=user_name, user_id=user_id, isWin=isWin)
        elif(button == "🔽"):
            last_views = self.last_music.views
            now_views = self.music.views
            isWin = False
            if now_views < last_views:
                self.max_rating += 1
                isWin = True
            self.last_music = self.music
            self.music = None
            return self.next_step(user_name=user_name, user_id=user_id, isWin=isWin)

    def start_message(self):
        return ReturnCommandObj("Оберіть категорію пісень", self.category_controller.get_list_category())


class DefoultSession(Session):
    def __init__(self, chat_id: str, mode: str, messager: str, host: str, category_controller: CategoryController):
        super().__init__(chat_id, mode, messager, host)
        self.category_controller = category_controller
        self.category = None
        self.music: Music = None
        self.last_music = None
        self.isNameUnswer = False
        self.isAuthorUnswer = False

    def next_step(self, text: str = "", user_name: str = "None", user_id: str = "None"):
        if not self.isUser(user_name, user_id):
            self.add_user(user_name, user_id)
        user: User = self.get_user(user_name, user_id)
        if self.music == None:
            self.music = self.category_controller.get_music_by_category(self.category)
            if self.last_music == None:
                return ReturnCommandObj("Вам надано 10 секунд пісні, спробуйте вгадати автора та назву", buttons=["_skip"], file=self.music.get_file())
            else:
                return ReturnCommandObj("Це була пісня: "+self.last_music.author+" - "+self.last_music.name+"\nВам надано 10 секунд пісні, спробуйте вгадати автора та назву",
                                        buttons=["_skip"], file=self.music.get_file())
        elif(self.category != None):
            if(WW_String.is_iqvals(self.music.name, text) and not WW_String.is_iqvals(self.music.author, text)):
                self.isNameUnswer = True
                if(self.isNameUnswer and self.isAuthorUnswer):
                    return ReturnCommandObj(replyText="Ви все вгадали! Супер! Йдемо далі!\n\nВам надано 10 секунд пісні, спробуйте вгадати автора та назву", buttons=["_skip"], file=self.music.get_file())
                else:
                    return ReturnCommandObj(replyText="Ви вгадали назву пісні, вітаю!")
            elif(not WW_String.is_iqvals(self.music.name, text) and WW_String.is_iqvals(self.music.author, text)):
                self.isAuthorUnswer = True
                if (self.isNameUnswer and self.isAuthorUnswer):
                    return ReturnCommandObj(replyText="Ви все вгадали! Супер! Йдемо далі!\n\nВам надано 10 секунд пісні, спробуйте вгадати автора та назву", buttons=["_skip"], file=self.music.get_file())
                else:
                    return ReturnCommandObj(replyText="Ви вгадали автора пісні, вітаю!")
            elif(WW_String.is_iqvals(self.music.name, text) and WW_String.is_iqvals(self.music.author, text)):
                self.isAuthorUnswer = False
                self.isNameUnswer = False
                self.music = None
                self.last_music = None
                self.music = self.category_controller.get_music_by_category(self.category)
                return ReturnCommandObj(replyText="Вау, ви вгадали і пісню, і автора. Супер! Йдемо далі!\n\nВам надано 10 секунд пісні, спробуйте вгадати автора та назву", buttons=["_skip"], file=self.music.get_file())


    def set_category(self, text: str, user_name: str = None, user_id: str = None):
        self.category = text
        return self.next_step(user_name=user_name, user_id=user_id)

    def click_button(self, button: str = "", user_name: str = "None", user_id: str = "None"):
        if(button.startswith("category_")):
            return self.set_category(button.split("_")[1], user_name=user_name, user_id=user_id)
        elif(button == "skip"):
            self.last_music = self.music
            self.isAuthorUnswer = False
            self.isNameUnswer = False
            self.music = None
            return self.next_step(user_name=user_name, user_id=user_id)

    def start_message(self):
        return ReturnCommandObj("Оберіть категорію пісень", self.category_controller.get_list_category())

class CommandController:
    def __init__(self):
        self.list_session_telegram: list[Session] = []
        self.list_session_discord: list[Session] = []
        self.categorysContraller = CategoryController(SL_Settings.load_obj("list_view", "options"))

    def get_session_by_id(self, id: str, where: str = "every"):
        if(where == "every" or where == "discord"):
            for i in self.list_session_discord:
                if i.get_id() == id:
                    return i
        if (where == "every" or where == "telegram"):
            for i in self.list_session_telegram:
                if i.get_id() == id:
                    return i
        return None

    def command_text(self, text: str, chat_id: str, user_name: str, user_id: str, messanger_name: str): #обработка ответов
        if(self.get_session_by_id(chat_id) == None):
            return None
        session: Session = self.get_session_by_id(chat_id)
        return session.next_step(text, user_name, user_id)

    def click_button(self, text: str, chat_id: str, user_name: str, user_id: str, messanger_name: str):
        if (self.get_session_by_id(chat_id) == None):
            return None
        session: Session = self.get_session_by_id(chat_id)
        return session.click_button(text, user_name, user_id)

    def add_session(self, session: Session):
        if(session.messager == "telegram"):
            self.list_session_telegram.append(session)
        elif(session.messager == "discord"):
            self.list_session_discord.append(session)

    def del_session(self, session: Session):
        if(self.get_session_by_id(session.get_id()) == None):
            return None
        if(session.messager == "telegram"):
            for i in self.list_session_telegram:
                if i.get_id() == session.chat_id:
                    self.list_session_telegram.remove(i)
        elif(session.messager == "discord"):
            for i in self.list_session_discord:
                if i.get_id() == session.chat_id:
                    self.list_session_discord.remove(i)

    def start_defoult_mode(self, chat_id: str, user_name: str, messanger_name: str):
        if self.get_session_by_id(chat_id) != None:
            return ReturnCommandObj("У вас вже почата гра, завершіть її командою /end")
        session = DefoultSession(chat_id, "defoult", messanger_name, user_name, self.categorysContraller) #standart_cat
        self.add_session(session)
        return session.start_message()

    def start_UpDown_mode(self, chat_id: str, user_name: str, messanger_name: str):
        if self.get_session_by_id(chat_id) != None:
            return ReturnCommandObj("У вас вже почата гра, завершіть її командою /end")
        session = UpDownSession(chat_id, "UpDown", messanger_name, user_name, self.categorysContraller)
        self.add_session(session)
        return session.start_message()

    def end_session(self, chat_id: str, user_name: str, user_id: str, messanger_name: str):
        if self.get_session_by_id(chat_id) == None:
            return None
        self.del_session(self.get_session_by_id(chat_id))
        return ReturnCommandObj("Гра завершена!")

    #def download_playlist(self, url: str, category_name: str, colvo: int):
    #    res = downloader.start_download_thread(url, category_name, colvo)
    #    if(res == "yes"):
    #        return ReturnCommandObj("Все окей! Найближчім часом ваш плейліст з'явиться у боті")
    #    else:
    #        return ReturnCommandObj("Хтось вже додає плейліст! Будь ласка спробуйте пізніше")

    def start_fight_mode(self):
        pass