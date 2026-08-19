def load_text(path):     #load text from a file
  with open(path, "r", encoding="utf-8") as f:
    return f.read()

def extract_chapters(text, n=3):     #extract the first n chapters
  parts = text.split("CHAPTER")[1:]
  selected = parts[:n]
  return "\n".join("CHAPTER" + p for p in selected)

def save_text(path, content):      #save text in a file
  with open(path, "w", encoding="utf-8") as f:
    f.write(content)

def run_extraction():   #the whole extraction Prozess
  raw = load_text(" ") #hier kommt die Wal Datei
  chapters = extract_chapters(raw, 3)
  save_text(" ", chapters) #hier kommt name wie gespeichert

#if __name__ == "__main__":  #starts automaticly running
  #run_extraction()
