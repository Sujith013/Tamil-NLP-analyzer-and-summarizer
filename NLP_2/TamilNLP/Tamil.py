import re
import nltk

class Tamil:
    _str = ""
    _str_arr = []
    length = 0

    #uyir_list eluthu
    uyir_list = list('அஆஇஈஉஊஎஏஐஒஓஔஃ')

    #Mei eluthu
    mei_list = ["க","ங","ச","ஞ","ட","ண","த","ந","ப","ம","ய","ர","ல","வ","ழ","ள","ற","ன"]

    #Ascii values for the characters like "்", "ெ", "ோ", "ீ"
    asc = [3021,3006,3007,3008,3009,3010,3014,3015,3016,3018,3019,3020]

    final_sentence = ()
    english_sentences =[]
    final_words = ()
    pos_tags = []
    root_word_count_1 = 0
    root_word_count_2 = 0

    digits = []
    prep = []
    prono = []
    NN = []
    VB = []
    PP = []
    AM = [] 
    tnse = []
    gdr = []
    wc = []

    sentences = []
    word_tokens = []
    clitics_removed = []

    sentence_number = 0

    def __init__(self,tamil_word) -> None:
        self._str = tamil_word

        #validate if it has proper tamil format encoding
        if not self.validate():
            raise ValueError("Not a proper Tamil encoding")

    def summarize(self):

        self.sentence_tokenizer()
        self.word_tokenizer()

        self.remove_clitics()
        
        self.identify_gender()
        self.identify_tense()
        self.prepositions()
        self.pronouns()
        self.transliterate()
        self.root_word()

        f = open("./TamilNLP/values.txt","w")

        f.write("first_sentence,words,gender,tense,pronouns,prepositions,nouns,ambi_nouns,verbs,digits")

        for i in range(self.sentence_number):
            if i==0:
                y=1
            else:
                y=0

            f.write("\n"+str(y)+","+str(self.wc[i])+","+str(self.gdr[i])+","+str(self.tnse[i])+","+str(self.prono[i])+
                ","+str(self.prep[i])+","+str(self.NN[i])+","+str(self.AM[i])+","+str(self.VB[i]+self.PP[i])+","+str(self.digits[i]))

        f.close()

    def sentence_tokenizer(self):
        self.sentences = nltk.sent_tokenize(self._str)

        self.sentence_number = len(self.sentences)
        self.final_sentence = tuple(self.sentences)
    
    def word_tokenizer(self):

        plist = [",",";",":","/","\\","(",")","[","]","{","}","*","+","-","_","=","@","#","$","%","^","&","*","|","/",
                 "~","`","?",".","<",">","'","\"","‘","’","!","@","#","$","%","^","&","*","+","=","\'","\""]

        for i in range(self.sentence_number):
            for p in plist:
                self.sentences[i] = self.sentences[i].replace(p,"")

        for x in self.sentences:
            self.word_tokens.append(nltk.word_tokenize(x))
            self.root_word_count_1+= len(nltk.word_tokenize(x))
            self.wc.append(len(nltk.word_tokenize(x)))

        self.final_words = tuple(self.word_tokens)

    def remove_clitics(self):
        words_new = []

        for r in self.word_tokens:
            d=0
            words_new = []

            for x in r:
                lp=0
                if x.isnumeric():
                    self.root_word_count_2+=1
                    words_new.append(x)
                    d+=1
                    continue
                
                if len(x)<=3:
                    continue

                last = x[len(x)-1]
                z = ord(last)

                thirdL = x[len(x)-3]
                z1 = ord(thirdL)

                if z1==3006 and z==3006 and len(x)>4: #remove "aada" sounds from the end 
                    x = x[0:len(x)-3] + chr(3021)

                if (x.endswith("வது") or x.endswith("னது")) and ord(x[len(x)-4]) == 3006 and len(x)>6:
                    x = x[0:len(x)-4] + chr(3021)
                    y = "ஆ" + x[-3:]
                    words_new.append(y)

                if (x.endswith("வது") or x.endswith("னது")) and x[len(x)-4].isnumeric():
                    x = x[len(x)-4]

                if (z==3006 or z==3015 or z==3019) and len(x)>4: # aa , ee and o sounds are removed
                    x = x[0:len(x)-1] + chr(3021)
                
                if x.endswith("சை") and len(x)>4:
                    x = x[0:len(x)-2]

                if x.endswith("னை") and len(x)>=4:
                    x = x[0:len(x)-1]+chr(3021)
                
                if x.endswith("வை") and len(x)>=4:
                    x = x[0:len(x)-1]+chr(3009)

                if x.endswith("கை") and len(x)>=4:
                    x = x[0:len(x)-1]+chr(3009)

                if x.endswith("ளை") and len(x)>=4:
                    x = x[0:len(x)-1]+chr(3021)                    

                if x.endswith("கள்") and len(x)>=5:
                    x = x[0:len(x)-3]
                
                if x.endswith("டைய") and len(x)>6: 
                    if x[len(x)-4] == chr(3009):
                        x = x[0:len(x)-4]+chr(3021) 

                if x.endswith("கம்") and len(x)>6:
                    if x[len(x)-4] in self.mei_list:
                        x = x[0:len(x)-3]+chr(3021)

                if x.endswith("க") and len(x)>4:
                    if x[len(x)-2] == chr(3006):
                        x = x[0:len(x)-2]+chr(3021)

                if x.endswith("ன") and len(x)>4:
                    if x[len(x)-2] == chr(3006):
                        x = x[0:len(x)-2]+chr(3021)

                if x[len(x)-1] == chr(3021) and x[len(x)-2] in ["க","ச","ட","த","ப","ற"]:
                    x = x[0:len(x)-2]
                
                words_new.append(x)

            self.digits.append(d)
            self.clitics_removed.append(words_new)

    def identify_gender(self):
        for r in self.clitics_removed:
            gdrs = 0
            
            for x in r:
                y = re.search("தான்|னான்|பான்|றான்|டான்|வான்|ணான்$",x)
                z = re.search("தாள்|னாள்|பாள்|றாள்|டாள்|வாள்|ணாள்$",x)
                
                if z!=None:
                    gdrs+=1
                if y!=None:
                    gdrs+=1

                if "அவள்" in r and "அவன்" in r:
                    gdrs+=2


                elif "அவள்" in r:
                    gdrs+=1

                elif "அவன்" in r:
                    gdrs+=1
            
            self.gdr.append(gdrs)

    def identify_tense(self):
        for r in self.clitics_removed:
            m=0

            for x in r:

                past = re.search("தான்|னான்|டான்|ணான்|தேன்|னேன்|டேன்|தார்|னார்|டார்$",x)
                present = re.search("றாள்|றான்|றேன்|றார்$",x)
                future = re.search("பான்|வான்|வாள்|பாள்|பேன்|வேன்|பார்|வார்$",x)

                if past!=None:
                    m+=1

                elif present!=None:
                    m+=1

                elif future!=None:
                    m+=1
            
            self.tnse.append(m)

    def prepositions(self):
        prepositions = ["ல","இல்","உள்ள","உள்ளே","மேல","மேலே","மேல்","அடியில","அடியில்","கீழ","கீழே","கீழ்",
                        "மூலம்","வாயிலாக","வழியாக","முன்","முன்னே","பின்","பின்னே","நடுவே","இடையில்","இடையே",
                        "வெளியில்","வெளியே","எல்லாம்","எதிரே","வழியே","வழி"]

        for r in self.clitics_removed:
            m=0
            
            for x in r:
                if x in prepositions:
                    m+=1     
                    self.root_word_count_2+=1
            
            self.prep.append(m)

    def pronouns(self):
        f = open("./TamilNLP/DataBase/pronouns.txt","r",encoding="utf-8")

        pronouns = f.readlines()

        pr_tamil = []
        pr_eng = []
        tmp = []

        for i in range(len(pronouns)):
            tmp = re.split(" ",pronouns[i])
            pr_tamil.append(tmp[0].rstrip())
            pr_eng.append(tmp[1].rstrip())

        f.close()

        for r in self.clitics_removed:
            m=0

            for x in r:
                if x in pr_tamil:
                    m+=1

            self.prono.append(m)

    def transliterate(self):

        eng1 = ["a","aa","i","ii","u","uu","e","ee","ai","o","oo","au","aK"]
        eng2 = ["k","nk","c","nc","t","Nn","th","n","p","m","y","r","l","v","z","L","R","N"] 

        for r in self.clitics_removed:
            temp = []
            
            for x in r:
                if x.isnumeric():
                    temp.append(x)
                    continue

                eg=""

                for y in x:
                    if y in self.uyir_list: 
                        ind = self.uyir_list.index(y)
                        eg+= eng1[ind]

                    elif y in self.mei_list:
                        ind = self.mei_list.index(y)
                        eg+= eng2[ind]+"a"

                    elif ord(y)==3021:
                        eg = eg[0:len(eg)-1]
                        continue

                    elif ord(y) in self.asc:
                        ind = self.asc.index(ord(y))
                        eg = eg[0:len(eg)-1]
                        eg+= eng1[ind]

                temp.append(eg)
            
            self.english_sentences.append(tuple(temp))
    
    def root_word(self):

        f1=open("./TamilNLP/DataBase/Noun.txt","r")
        f2=open("./TamilNLP/DataBase/verb.txt","r")
        f3=open("./TamilNLP/DataBase/pp.txt","r")
        f4=open("./TamilNLP/DataBase/AmbiNoun.txt","r")
        f5=open("./TamilNLP/DataBase/case.txt","r")

        nounList = f1.readlines()
        verbList = f2.readlines()
        ppList = f3.readlines()
        ambiList = f4.readlines()
        caseList = f5.readlines()

        for i in range(len(nounList)):
            nounList[i] = nounList[i].rstrip()

        for i in range(len(verbList)):
            verbList[i] = verbList[i].rstrip()

        for i in range(len(ppList)):
            ppList[i] = ppList[i].rstrip()

        for i in range(len(ambiList)):
            ambiList[i] = ambiList[i].rstrip()

        for i in range(len(caseList)):
            caseList[i] = caseList[i].rstrip()

        for r in self.english_sentences:
            nn =0
            vb =0
            pp=0
            am =0

            for x in r:
                if x in nounList:
                    self.root_word_count_2+=1
                    nn+=1

                if x in verbList:
                    self.root_word_count_2+=1
                    vb+=1

                if x in ppList:
                    self.root_word_count_2+=1
                    pp+=1

                if x in ambiList:
                    self.root_word_count_2+=1
                    am+=1
            
            self.NN.append(nn)
            self.VB.append(vb)
            self.PP.append(pp)
            self.AM.append(am)

        f1.close()
        f2.close()
        f3.close()
        f4.close()
        f5.close()

    def validate(self) -> bool:

        if len(self._str) == 0:
            return True

        prev = True if ord(self._str[0]) in self.asc else False

        if prev:
            return False
        
        for i in range(1,len(self._str)):
            if ord(self._str[i]) in self.asc:
                if prev:
                    return False
                prev = True
            
            else:
                prev = False

        return True

    def remove_digits(self):
        self.digits_count = 0

        nlist = ['0','1','2','3','4','5','6','7','8','9']

        for n in nlist:
            self._str = self._str.replace(n,"")

        self.form_array()
        
        return self._str

    def __str__(self):
        return self._str

    def __len__(self) -> int:
        return self.length

    def __getitem__(self,key):
        if key<self.length:
            return self._str_arr[key]
        else:
            raise ValueError("Index out of bound")

    def __setitem__(self,key,ch):
        #if empty ch remove the index
        if key<self.length:
            if len(ch)<=2:
                if len(ch)==1:
                    if ord(ch) in self.asc:
                        raise ValueError("Not a proper charcter")
                    else:
                        self._str_arr[key] = ch
                        self._str = "".join(self._str_arr)

                else:
                    if (ord(ch[0]) in self.asc and ord(ch[1]) in self.asc) or (ord(ch[0]) not in self.asc and ord(ch[1]) not in self.asc):
                        raise ValueError("Not a valid character")
                    
                    if ord(ch[0]) in self.asc:
                        raise ValueError("Not a valid Tamil Character")
                
                    self._str_arr[key] = ch
                    self._str = "".join(self._str_arr)
            else:
                raise ValueError("Only Character is allowed")
        else:
            raise ValueError("Index Out of Bound")


    def __iter__(self):
        
        for i in self._str_arr:
            yield i

