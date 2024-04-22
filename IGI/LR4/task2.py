import re
import zipfile

class MyTextAnalyzerMixin:
    """Mixin for text analyzing"""
    def words_lowercase_diggits(self):
        """Method for finding words consisting of lowercase letters and diggits"""
        words = re.findall(r'\b[а-яa-z0-9]*[а-яa-z][0-9][a-zа-я0-9]*\b|\b[0-9][a-zа-я0-9]*[a-zа-я][a-zа-я0-9]*\b', self.text)
        return words
    
    def ipv4(self):
        """Method for finding ipv4"""
        ips = re.findall(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b', self.text)
        return ips
    
    def count_short_words(self):
        """Method for counting short words"""
        words = re.findall('[a-zA-Zа-яА-Я0-9]{6,}', self.text)
        return len(words)
    
    def shortest_word_with_last_w(self):
        """Method for finding shortest word ending w"""
        words = re.findall('[а-яА-Яa-zA-Z0-9]*w', self.text)
        best = 1e9
        result = ''
        for word in words:
            if len(word) < best:
                result = word
                best = len(word)
        return result
    
    def all_words(self):
        """Method for finding all words"""
        words = re.findall('[a-zA-Zа-яА-Я0-9]+', self.text)
        return sorted(words, key=len)

class TextAnalyzer(MyTextAnalyzerMixin):
    """Class for text analyzing"""
    def __init__(self, text):
        self.text = text

    def count_sentences(self):
        """Method for counting sentences"""
        sentences = re.findall(r'[.!?]\s*', self.text)
        return len(sentences)
    
    def count_sentence_types(self):
        """Method for counting sentence types"""
        pov = len(re.findall(r'[.]\s*', self.text))
        vopr = len(re.findall(r'[?]\s*', self.text))
        voskl = len(re.findall(r'[!]\s*', self.text))
        return pov, vopr, voskl
    
    def average_sentence_length(self):
        """Method for finding average sentence length"""
        sentences = re.split(r'[.!?][\n\s]*', self.text)
        symbols = 0
        count = 0
        for sentence in sentences:
            words = re.findall(r'\b[a-zA-Zа-яА-Я0-9]+\b', sentence)
            for word in words:
                symbols += len(word)
            if words:
                count += 1
        
        if count == 0:
            return 0    
        
        return symbols / count

    def average_word_length(self):
        """Method for finding average word length"""
        words = re.findall(r'\b[a-zA-Zа-яА-Я0-9]+\b', self.text)
        symbols = 0
        for word in words:
            symbols += len(word)
        return symbols / len(words)
    
    def count_smiles(self):
        """Method for counting smiles"""
        smiles = re.findall(r'[;:]-*[\(\[\)\]]+', self.text)
        return len(smiles) 

class Archiever:
    """Class for archieve data"""
    @staticmethod
    def archieve(filename, filename_zip, results):
        """Method for zipping results"""
        try:
            with zipfile.ZipFile(filename_zip, 'w') as zip_file:
                with open(filename, 'w', encoding='utf-8') as file:
                    for key, value in results.items():
                        file.write(key + ":" + str(value) + "\n")
                zip_file.write(filename)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    @staticmethod
    def get_info(filename):
        """Method for getting info from zip"""
        try:
            with zipfile.ZipFile(filename, 'r') as zip_file:
                for info in zip_file.infolist():
                    file_content = zip_file.read(info.filename).decode('utf-8')  
                    print(f"Filename: {info.filename}")
                    print(f"File size: {info.file_size}")
                    print(f"Compressed size: {info.compress_size}")
                    print(f"Compress type: {info.compress_type}")
                    print(f"Content:\n{file_content}\n")  
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    

def main():
    filename = 'LR4/text.txt'
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    analyzer = TextAnalyzer(text)
    
    sentences = analyzer.count_sentences()
    print('Sentences number =', sentences)
    
    print()
    
    narrative, exclamatory, interrogative = analyzer.count_sentence_types()
    print(f'Narrative: {narrative} Exclamination: {exclamatory} Interrogative: {interrogative}')
    
    print()
    
    average_sentence_length = analyzer.average_sentence_length()
    print('Average sentence leghth =', average_sentence_length)
    
    print()
    
    average_word_length = analyzer.average_word_length()
    print('Average word length =',average_word_length)
    
    print()
    
    smiles = analyzer.count_smiles()
    print('Count of smiles =', smiles)
    
    print()
   
    words_lowercase_diggits = analyzer.words_lowercase_diggits()
    print('Words with lowercaase and diggits')
    for word in words_lowercase_diggits:
        print(word)
    
    print()
    
    ips = analyzer.ipv4()
    print('IPV4')
    for ip in ips:
        print(ip)
       
    print()
       
    short_words = analyzer.count_short_words()
    print('Count of words less than 6 symbols =', short_words)
    
    print()
    
    shortest_word_end_w = analyzer.shortest_word_with_last_w()
    print('The shortest word ending with w', shortest_word_end_w)
    
    print()
    
    all_words = analyzer.all_words()
    print('Words sorted by length')
    for word in all_words:
        print(word)
        
    results = {
        "sentences":sentences,
        "narrative":narrative,
        "exclamatory":exclamatory,
        "interrogative":interrogative,
        "average_sentence_length":average_sentence_length,
        "average_word_length":average_word_length,
        "smiles":smiles,
        "ips":ips,
        "short_words":short_words,
        "shortest_word_end_w":shortest_word_end_w,
        "all_words":all_words
    }

    
    filename_output = "LR4/results.txt"
    filename_output_zip = "LR4/results.zip"
    
    Archiever.archieve(filename_output, filename_output_zip, results)
    Archiever.get_info(filename_output_zip)

if __name__ =="__main__":
    main()