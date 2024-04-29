from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMessageBox as qmb
import random
import sys

cls, wnd = uic.loadUiType("okno6.ui")


class Wordle(wnd, cls):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Wordle game")
        self.gamePrep()

    @pyqtSlot()
    def clearGame(self):
        for i in range(30):
            self.rounds[i].clear()

    @pyqtSlot()
    def on_actionRestart_triggered(self):
        self.clearGame()
        self.gamePrep()

    @pyqtSlot()
    def gamePrep(self):
        self.getWord()
        self.label.setVisible(False)
        self.pushButton3.setVisible(False)
        self.rounds = [self.s1, self.s2, self.s3, self.s4, self.s5,
                       self.s6, self.s7, self.s8, self.s9, self.s10,
                       self.s11, self.s12, self.s13, self.s14, self.s15,
                       self.s16, self.s17, self.s18, self.s19, self.s20,
                       self.s21, self.s22, self.s23, self.s24, self.s25,
                       self.s26, self.s27, self.s28, self.s29, self.s30]

        self.roundNum=1
        for i in self.rounds[0:5]:
            i.setEnabled(True)
        self.s1.setFocus()
        for i in self.rounds[5:30]:
            i.setEnabled(False)

        for i in self.rounds:
            i.setStyleSheet("background-color: #d3d8df; color: black; border-radius: 15px")

        for i in range(len(self.rounds) - 1):
            self.rounds[i].textChanged.connect(lambda _, index=i: self.focusNextLineEdit(index))

        for line_edit in self.rounds:
            line_edit.textEdited.connect(self.onTextEdited)


        # for i in range(len(self.rounds)):
        #     if i>0:
        #         self.rounds[i].keyPressEvent = lambda event, index=i: self.keyPressEvent(event, index)


    # @pyqtSlot()
    # def keyPressEvent(self, event, current_index):
    #     if event.key() in (Qt.Key_Return, Qt.Key_Enter):
    #         self.on_pushButton_clicked()
    #     elif event.key() == Qt.Key_Backspace:
    #         print("back")
    #         current_round_edit = self.rounds[current_index]
    #         previous_index = (current_index - 1) % len(self.rounds)
    #         previous_round_edit = self.rounds[previous_index]
            
    #         if len(current_round_edit.text()) == 0:
    #             previous_round_edit.setFocus()
      

    @pyqtSlot()
    def focusNextLineEdit(self, current_index):
        current_round_edit = self.rounds[current_index]
        next_index = (current_index + 1) % len(self.rounds)
        next_round_edit = self.rounds[next_index]
        
        if len(current_round_edit.text()) > 0:
            next_round_edit.setFocus()

    @pyqtSlot(str)
    def onTextEdited(self, newText):
        sender = self.sender()
        sender.setText(newText.upper())

    @pyqtSlot()
    def getWord(self):
        self.wordsFile = open("words-wordle.txt", "r")
        words = self.wordsFile.read().splitlines()
        self.wordsFile.close()
        self.gameWord = random.choice(words)
        print(self.gameWord)


    @pyqtSlot()
    def checkWord(self, letters):
        idx = 0
        for i in letters:
            if i.text() != self.gameWord[idx]:
                i.setStyleSheet("background-color: #adb5bd; color: white; border-radius: 15px")
            for j in self.gameWord:
                if i.text() == j:
                    i.setStyleSheet("background-color: orange; color: white; border-radius: 15px")      
            if i.text() == self.gameWord[idx]:
                i.setStyleSheet("background-color: green; color: white; border-radius: 15px")
            idx += 1

        
    @pyqtSlot()
    def checkInput(self, round, nextRound):
        word=[]
        self.ifWin=''
        for i in round:
            if not i.text().isalpha():
                qmb.information(None, "Alert", "Please fill in all fields and make sure you only enter letters!")
                return
        for i in round:
            word.append(i.text())
        word = ''.join(word)
        self.wordsFile = open("valid-wordle-words.txt", "r")
        if word == self.gameWord:
            for i in round:
                i.setStyleSheet("background-color: green; color: white; border-radius: 15px")
            response = qmb.question(None, "Alert", "You WON! Congratulations!\nDo you want to play again?", qmb.Yes | qmb.No)
            if response == qmb.Yes:
                self.clearGame()
                self.gamePrep()
            else:
                qmb.information(None, "Alert", "Thank you for playing!")
                sys.exit()
        else:
            if word in self.wordsFile.read():
                    self.checkWord(round)
                    self.roundNum += 1
                    for i in round:
                        i.setEnabled(False)
                    for i in nextRound:
                        i.setEnabled(True)
                    self.ifWin='F'
            else:
                qmb.information(None, "Alert", "Not a word! Try again!")
        self.wordsFile.close()
        

    @pyqtSlot()
    def on_pushButton_clicked(self):
        if self.roundNum == 1:
            self.checkInput(round=self.rounds[0:5], nextRound=self.rounds[5:10])
            self.s6.setFocus()
        elif self.roundNum == 2:
            self.checkInput(round=self.rounds[5:10], nextRound=self.rounds[10:15])
            self.s11.setFocus()
        elif self.roundNum == 3:
            self.checkInput(round=self.rounds[10:15], nextRound=self.rounds[15:20])
            self.s16.setFocus()
        elif self.roundNum == 4:
            self.checkInput(round=self.rounds[15:20], nextRound=self.rounds[20:25])
            self.s21.setFocus()
        elif self.roundNum == 5:
            self.checkInput(round=self.rounds[20:25], nextRound=self.rounds[25:30])
            self.s26.setFocus()
        elif self.roundNum == 6:
            self.checkInput(round=self.rounds[25:30], nextRound=self.rounds[25:30])
            if self.ifWin == 'F':
                response = qmb.question(None, "Alert", f"Unfortunately!\nThe word was: \n{self.gameWord}\nDo you want to play again?", qmb.Yes | qmb.No)
                if response == qmb.Yes:
                    self.clearGame()
                    self.gamePrep()
                else:
                    qmb.information(None, "Alert", "Thank you for playing!")
                    sys.exit()

    
    @pyqtSlot()
    def on_pushButton2_clicked(self):
        response = qmb.question(None, "Alert", f"Unfortunately!\nThe word was: \n{self.gameWord}\nDo you want to play again?", qmb.Yes | qmb.No)
        if response == qmb.Yes:
            self.clearGame()
            self.gamePrep()
        else:
            qmb.information(None, "Alert", "Thank you for playing!")
            sys.exit()


    @pyqtSlot()
    def on_pushButton3_clicked(self):
        self.clearGame()
        self.gamePrep()
         
    @pyqtSlot()
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.on_pushButton_clicked()

    @pyqtSlot()
    def on_actionRules_triggered(self):
        self.label.setVisible(True)
        self.pushButton3.setVisible(True)

    @pyqtSlot()
    def on_actionExit_triggered(self):
        sys.exit()

    
if __name__ == '__main__':
    game = QApplication([])
    okno = Wordle()
    okno.show()
    game.exec()
