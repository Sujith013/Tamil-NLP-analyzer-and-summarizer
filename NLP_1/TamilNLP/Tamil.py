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

    def sentence_tokenizer(self):
        k=0

        self.sentences = nltk.sent_tokenize(self._str)

        self.sentence_number = len(self.sentences)
        self.final_sentence = tuple(self.sentences)

        print("Tokenized Sentences")
        print("")
        print(self.final_sentence)
        print("\n\n")
    
    def word_tokenizer(self):

        plist = [",",";",":","/","\\","(",")","[","]","{","}","*","+","-","_","=","@","#","$","%","^","&","*","|","/","~","`","?",".","<",">","'","\"","‘","’"]

        for i in range(self.sentence_number):
            for p in plist:
                self.sentences[i] = self.sentences[i].replace(p,"")

        print("Punctuations Removed")
        print("")
        print(self.sentences)
        print("\n\n")

        for x in self.sentences:
            self.word_tokens.append(nltk.word_tokenize(x))
            self.root_word_count_1+= len(nltk.word_tokenize(x))
            
        self.final_words = tuple(self.word_tokens)
        
        print("Tokenized words")
        print("")
        print(self.final_words)
        print("\n\n")

    def remove_clitics(self):
        words_new = []

        for r in self.word_tokens:

            words_new = []

            for x in r:
                if x.isnumeric():
                    self.root_word_count_2+=1
                    words_new.append(x)
                    continue
                
                if len(x)<=3:
                    continue

                last = x[len(x)-1]
                z = ord(last)

                thirdL = x[len(x)-3]
                z1 = ord(thirdL)

                if z1==3006 and z==3006 and len(x)>4: #remove "aada" sounds from the end 
                    y = x[0:len(x)-3] + chr(3021)
                    words_new.append(y)

                elif (x.endswith("வது") or x.endswith("னது")) and ord(x[len(x)-4]) == 3006 and len(x)>6:
                    words_new.append(x[0:len(x)-4] + chr(3021))
                    y = "ஆ" + x[-3:]
                    words_new.append(y)

                elif (x.endswith("வது") or x.endswith("னது")) and x[len(x)-4].isnumeric():
                    words_new.append(x[len(x)-4])

                elif z==3006 or z==3015 or z==3019: # aa , ee and o sounds are removed
                    y = x[0:len(x)-1] + chr(3021)
                    words_new.append(y)
                
                elif x.endswith("சை") and len(x)>4:
                    words_new.append(x[0:len(x)-2])

                elif x.endswith("னை") and len(x)>=4:
                    words_new.append(x[0:len(x)-1]+chr(3021))
                
                elif x.endswith("வை") and len(x)>=4:
                    words_new.append(x[0:len(x)-1]+chr(3009))

                elif x.endswith("கை") and len(x)>=4:
                    words_new.append(x[0:len(x)-1]+chr(3009))
                
                elif x.endswith("கள்") and len(x)>=5:
                    if x[len(x)-4] == chr(3021):
                        words_new.append(x[0:len(x)-5])
                    else:
                        words_new.append(x[0:len(x)-3])
                
                elif x.endswith("டைய") and len(x)>6: 
                    if x[len(x)-4] == chr(3009):
                        words_new.append(x[0:len(x)-4]+chr(3021)) 

                elif x.endswith("கம்") and len(x)>6:
                    if x[len(x)-4] in self.mei_list:
                        words_new.append(x[0:len(x)-3]+chr(3021))

                elif x.endswith("க") and len(x)>4:
                    if x[len(x)-2] == chr(3006):
                        words_new.append(x[0:len(x)-2]+chr(3021))

                elif x.endswith("ன") and len(x)>4:
                    if x[len(x)-2] == chr(3006):
                        words_new.append(x[0:len(x)-2]+chr(3021))

                else:
                    words_new.append(x)

            self.clitics_removed.append(words_new)

        print("Clitics Removed")
        print("")
        print(self.clitics_removed)
        print("\n\n")

    def identify_gender(self):
        m=""

        print("Gender Identification")
        print("")

        k=0

        for r in self.clitics_removed:
            k+=1
            m=""
            
            for x in r:
                y = re.search("தான்|னான்|பான்|றான்|டான்|வான்|ணான்$",x)
                z = re.search("தாள்|னாள்|பாள்|றாள்|டாள்|வாள்|ணாள்$",x)

                if len(x)>6:

                    if (z!=None):
                        if m=="female" or m=="b":
                            continue
                        elif m=="male":
                            m="b"
                        else:
                            m="female"

                        print(x)

                    elif (y!=None):
                        if m=="male" or m=="b":
                            continue
                        elif m=="female":
                            m="b"
                        else:
                            m="male"

                        print(x)

                if m=="b":
                    break

                if "அவள்" in r and "அவன்" in r:
                    m="b"
                    print("அவள்")
                    print("அவன்")


                elif "அவள்" in r:
                    if m=="male":
                        m="b"
                        print("அவள்")
                    else:
                        m="female"

                elif "அவன்" in r:
                    if m=="female":
                        m="b"
                        print("அவன்")
                    else:
                        m="male"

            if m=="b":
                print("sentence "+str(k)+" : ",end="")
                print("Both genders identified")

            elif m=="male":
                print("sentence "+str(k)+" : ",end="")                
                print("Male specific")

            elif m=="female":
                print("sentence "+str(k)+" : ",end="")
                print("Female specific")
            
        print("\n\n")

    def identify_tense(self):
        m = []
        xy = []

        print("Tense Identification")
        print("")

        k=0

        for r in self.clitics_removed:
            k+=1

            m=[]
            xy=[]

            for x in r:

                past = re.search("தான்|னான்|டான்|ணான்|தேன்|னேன்|டேன்|தார்|னார்|டார்$",x)
                present = re.search("றாள்|றான்|றேன்|றார்$",x)
                future = re.search("பான்|வான்|வாள்|பாள்|பேன்|வேன்|பார்|வார்$",x)

                if past!=None:
                    m.append("p")
                    xy.append(x)

                elif present!=None:
                    m.append("pr")
                    xy.append(x)

                elif future!=None:
                    m.append("f")
                    xy.append(x)

            if len(m)==0:
                fT=""
            else:
                print("sentence "+str(k)+" : ",end="")
                fT = max(m,key=m.count)
                print(xy,end="")
                print(" ",end="")
                print(m,end="")
                print(" ",end="")   

            if fT=="p":
                print("Past")

            elif fT=="pr":    
                print("Present")

            elif fT=="f":    
                print("Future")

        print("\n\n")

    def prepositions(self):
        
        print("Prepositions and conjungtions")
        print("")

        k=0

        prepositions = ["ல","இல்","உள்ள","உள்ளே","மேல","மேலே","மேல்","அடியில","அடியில்","கீழ","கீழே","கீழ்",
                        "மூலம்","வாயிலாக","வழியாக","முன்","முன்னே","பின்","பின்னே","நடுவே","இடையில்","இடையே",
                        "வெளியில்","வெளியே","எல்லாம்","எதிரே","வழியே","வழி"]
        
        prp_eng = ["in","in","inside","inside","on","on","on","under","under","under","under","under",
                   "through","through","thorugh","front","ahead","after","behind","between","between","between",
                   "outside","outside","all","opposite","through","through"]

        for r in self.clitics_removed:
            k+=1

            for x in r:
                z=0

                if x in prepositions:
                    if z==0:
                        print("sentence "+str(k))
                        z=1

                    self.root_word_count_2+=1
                    print(x+" - ",end="")

                    t = prepositions.index(x)

                    print(prp_eng[t])

        print("\n")

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

        print("Pronouns")
        print("")

        k=0

        for r in self.clitics_removed:
            z=0
            k+=1

            for x in r:
                if x in pr_tamil:
                    if z==0:
                        print("sentence "+str(k)+":")
                        z=1

                    t = pr_tamil.index(x)
                    print("     "+pronouns[t])
        
        print("\n")

    def transliterate(self):

        eng1 = ["a","aa","i","ii","u","uu","e","ee","ai","o","oo","au","aK"]
        eng2 = ["k","nk","c","nc","t","Nn","th","n","p","m","y","r","l","v","z","L","R","N"] 

        print("Transliterated Words\n")

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

        print(self.english_sentences)
        print("\n\n")
    
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

        print("\nNouns\n")

        for r in self.english_sentences:
            for x in r:
                if x in nounList:
                    self.root_word_count_2+=1
                    print(x)
        
        print("\nVerbs\n")

        for r in self.english_sentences:
            for x in r:
                if x in verbList:
                    self.root_word_count_2+=1
                    print(x)

        print("\nPast pasrticiples\n")

        for r in self.english_sentences:
            for x in r:
                if x in ppList:
                    self.root_word_count_2+=1
                    print(x)
        
        print("\nAmbiguos Nouns\n")

        for r in self.english_sentences:
            for x in r:
                if x in ambiList:
                    self.root_word_count_2+=1
                    print(x)

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

