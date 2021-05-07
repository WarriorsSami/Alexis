from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common import action_chains

from WebDriverCreator import WebDriverCreator
import time
import pymongo


class App:
    def __init__(self, config):

        self.driver1 = WebDriverCreator.create(config["browser"])
        # self.driver2 = WebDriverCreator.create(config["browser"])
        self.config = config
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.userDB = self.client[self.config["mongoDB"]]
        self.userCollection = self.userDB[self.config["mongoCollection"]]
        self.problemCollection = self.userDB[self.config["mongoCollectionSolve"]]

    def run_for_users(self):
        try:
            self.login(self.config['userSrc'], self.driver1)
            self.populateDBFromTop100()
            self.populateDB()

            self.close()
        except Exception:
            try:
                self.driver1.close()
            except Exception:
                pass

            self.driver1 = WebDriverCreator.create(self.config["browser"])
            self.run_for_users()

    def run_for_code_download(self):
        try:
            self.login(self.config['userSrc'], self.driver1)
            self.get_submissions(self.config['userSrc'])
            self.get_code()

            self.close()
        except Exception:
            try:
                self.driver1.close()
            except Exception:
                pass

            self.driver1 = WebDriverCreator.create(self.config["browser"])
            self.run_for_code_download()

    def run_for_code_upload(self):
        try:
            self.login(self.config['userDest'], self.driver1)
            self.deploy_code()

            self.close()
        except Exception:
            try:
                self.driver1.close()
            except Exception:
                pass

            self.driver1 = WebDriverCreator.create(self.config["browser"])
            self.run_for_code_upload()

    def clearDBUsers(self):
        self.userCollection.remove({})

    def clearDBSubmissions(self):
        self.problemCollection.remove({})

    def print_lang(self):
        submissions = self.problemCollection.find()

        for submission in submissions:
            lang = submission["language"]
            pos = lang.find('.') + 1
            print(lang[pos:])

    @staticmethod
    def get_lang(arg):
        mapping = {
            "cpp": 1,
            "c": 2,
            "pas": 3,
            "php": 4,
            "py": 5,
            "py3": 6,
            "java": 7
        }

        return mapping.get(arg, "nope")

    def deploy_code(self):
        submissions = self.problemCollection.find({"executed": False})

        for submission in submissions:
            if submission["executed"] is True:
                continue

            self.driver1.get(submission["problem"])

            try:
                lang_id = self.get_lang(submission["language"])
                option = self.driver1.find_element_by_xpath(
                    '//*[@id="limbaj_de_programare"]/option[' + str(lang_id) + ']')
                option.click()
            except NoSuchElementException:
                pass

            # self.driver1.find_element_by_xpath('//*[@id="form-incarcare-solutie"]/div[2]/div/div[6]/div['
            #                                   '1]/div/div/div').click()

            # textArea = self.driver1.find_element_by_xpath('//*[@id="sursa"]')
            # textArea.send_keys(submission["code"])

            codeMirror = self.driver1.find_element_by_xpath('//*[@id="form-incarcare-solutie"]/div[2]/div/div[6]/div['
                                                            '1]/div/div/div')
            action = ActionChains(self.driver1)
            action.click(on_element=codeMirror)
            action.send_keys(submission["code"])
            action.perform()

            # action_chains.click(codeMirror).perform()
            # action_chains.send_keys(submission["code"]).perform()

            submitBtn = self.driver1.find_element_by_xpath('//*[@id="btn-submit"]')
            submitBtn.click()

            query = {"eval": submission["eval"]}
            values = {"$set": {"executed": True}}
            self.problemCollection.update_one(query, values)

            time.sleep(10)

        time.sleep(self.config["timeToWait"])

    def get_code(self):
        submissions = self.problemCollection.find({"code": ""})

        for submission in submissions:
            self.driver1.get(submission["eval"])
            code = self.driver1.find_element_by_xpath('//*[@id="sursa"]/pre').text
            lang = self.driver1.find_element_by_xpath('//*[@id="detalii"]/table/tbody/tr[4]/td[1]').text
            pos = lang.find('.') + 1
            print(code)
            print(lang)
            query = {"eval": submission["eval"]}
            values = {"$set": {"code": code, "language": lang[pos:]}}
            self.problemCollection.update_one(query, values)
            # print(submission["code"])

        time.sleep(self.config["timeToWait"])

    def get_submissions(self, user):

        for i in range(9, self.config['pagesForSubmissions']):
            self.driver1.get("https://www.pbinfo.ro/solutii/user/" + user['username'] + "?start=" + str(i * 50))

            for j in range(1, 51):
                try:
                    elem = {
                        "problem": self.driver1.find_element_by_xpath('//*[@id="zona-mijloc"]/div/div['
                                                                      '5]/table/tbody/tr[' +
                                                                      str(j) + ']/td[4]/a').get_property('href'),
                        "eval": self.driver1.find_element_by_xpath('//*[@id="zona-mijloc"]/div/div[5]/table/tbody/tr[' +
                                                                   str(j) + ']/td[6]/a').get_property('href'),
                        "status": self.driver1.find_element_by_xpath(
                            '//*[@id="zona-mijloc"]/div/div[5]/table/tbody/tr[' +
                            str(j) + ']/td[7]').text,
                        "code": "",
                        "language": "",
                        "executed": False
                    }

                    # problemToken = {"name": elem["problem"], "sub_link": elem["eval"], "status": elem["status"],
                    # "code": ""}

                    dbElem = self.problemCollection.count({"eval": elem["eval"]})
                    if elem["status"] != "100" or dbElem != 0:
                        continue

                    print(elem)
                    self.problemCollection.insert_one(elem)
                except NoSuchElementException:
                    pass

        time.sleep(self.config["timeToWait"])

    def login(self, user, driver):

        try:
            driver.get("https://www.pbinfo.ro/")
            emailField = driver.find_element_by_id("user")
            emailField.send_keys(user['username'])

            passwordField = driver.find_element_by_id("parola")
            passwordField.send_keys(user['password'])

            # the login button is the last element with the css selector ".form-group button[type='submit']"
            formGroupButtons = driver.find_elements_by_css_selector(".form-group button[type='submit']")
            formGroupButtons[len(formGroupButtons) - 1].click()

            time.sleep(self.config["timeToWait"])
        except NoSuchElementException:
            pass

    def populateDB(self):

        for i in range(0, self.config["pagesToSend"]):
            self.driver1.get("https://www.pbinfo.ro/solutii?start=" + str(i * 50))

            users = self.driver1.find_elements_by_css_selector(".pbi-widget-user a")

            for user in users:
                # the following chunk of code retrieves the user name
                userName = user.get_property('href')[len("https://www.pbinfo.ro/profil/"):]

                if userName in self.config["blacklist"]:
                    print("I have avoided " + userName)
                    continue
                else:
                    userToken = {"name": userName, "send-status": "false"}

                    dbElem = self.userCollection.count({"name": userName})
                    if dbElem == 0:
                        self.userCollection.insert_one(userToken)

    def populateDBFromTop100(self):

        self.driver1.get("https://www.pbinfo.ro/top100/dolj")

        users = self.driver1.find_elements_by_css_selector(".pbi-widget-user a")

        for user in users:
            # the following chunk of code retrieves the user name
            userName = user.get_property('href')[len("https://www.pbinfo.ro/profil/"):]

            if userName in self.config["blacklist"]:
                print("I have avoided " + userName)
                continue
            else:
                userToken = {"name": userName, "send-status": "false"}

                dbElem = self.userCollection.count({"name": userName})
                if dbElem == 0:
                    self.userCollection.insert_one(userToken)

    def sendMessagesToAllUsers(self):

        users = self.userCollection.find()
        for user in users:
            if user["send-status"] == "false":
                self.driver1.get('https://www.pbinfo.ro/?pagina=conversatii&partener=' + user["name"])

                try:
                    textArea = self.driver1.find_element_by_css_selector("#mesaj")
                    textArea.send_keys(self.config["messages"])

                    submitBtn = self.driver1.find_element_by_css_selector("input[value='Postează']")
                    submitBtn.click()

                    time.sleep(self.config["timeToWait"])

                    query = {"name": user["name"]}
                    values = {"$set": {"send-status": "true"}}
                    self.userCollection.update_one(query, values)

                except NoSuchElementException:
                    pass

    def sendMessagesToDiscord(self):

        users = self.config["discord"]
        for user in users:
            try:
                for i in range(0, 100):
                    for message in self.config["messages"]:
                        self.driver1.get('https://www.pbinfo.ro/?pagina=conversatii&partener=' + user)

                        # write the message in the text area element
                        textArea = self.driver1.find_element_by_css_selector("#mesaj")

                        textArea.send_keys(message)
                        # submit the message
                        submitBtn = self.driver1.find_element_by_css_selector("input[value='Postează']")
                        submitBtn.click()

                        time.sleep(self.config["timeToWait"])

                """
                self.driver.get('https://www.pbinfo.ro/?pagina=conversatii&partener=' + user)
                for message in self.config["messages"]:

                    textArea = self.driver.find_element_by_css_selector("#mesaj")

                    textArea.send_keys(message)

                    submitBtn = self.driver.find_element_by_css_selector("input[value='Postează']")
                    submitBtn.click()
                """

            except NoSuchElementException:
                pass

    def close(self):
        self.driver1.close()
        # self.driver2.close()
