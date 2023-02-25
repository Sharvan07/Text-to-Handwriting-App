from flask import Flask, render_template, request, send_file
from PIL import Image
from fpdf import FPDF

app = Flask(__name__)

BG = Image.open("mlfont/bg.png")
sizeOfSheet = BG.width
gap, _ = 0, 0
allowedChars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,.-?!() 1234567890'

def writee(char):
    global gap, _
    if char == '\n':
        pass
    else:
        char.lower()
        cases = Image.open("mlfont/%s.png" % char)
        BG.paste(cases, (gap, _))
        size = cases.width
        gap += size
        del cases

def letterwrite(word):
    global gap, _
    if gap > sizeOfSheet - 95 * (len(word)):
        gap = 0
        _ += 200
    for letter in word:
        if letter in allowedChars:
            if letter.islower():
                pass
            elif letter.isupper():
                letter = letter.lower()
                letter += 'upper'
            elif letter == '.':
                letter = "fullstop"
            elif letter == '!':
                letter = 'exclamation'
            elif letter == '?':
                letter = 'question'
            elif letter == ',':
                letter = 'comma'
            elif letter == '(':
                letter = 'braketop'
            elif letter == ')':
                letter = 'braketcl'
            elif letter == '-':
                letter = 'hiphen'
            writee(letter)

def worddd(Input):
    wordlist = Input.split(' ')
    for i in wordlist:
        letterwrite(i)
        writee('space')

def generate_pdf(data):
    global BG, gap, _
    l = len(data)
    nn = len(data) // 600
    chunks, chunk_size = len(data), len(data) // (nn + 1)
    p = [data[i:i + chunk_size] for i in range(0, chunks, chunk_size)]
    imagelist = []
    for i in range(0, len(p)):
        worddd(p[i])
        writee('\n')
        BG.save('%doutt.png' % i)
        imagelist.append('%doutt.png' % i)
        BG1 = Image.open("mlfont/bg.png")
        BG = BG1
        gap = 0
        _ = 0
    pdf = FPDF()
    for image in imagelist:
        pdf.add_page()
        pdf.image(image, 0, 0, 210, 297)
    pdf.output('output.pdf', 'F')
    for image in imagelist:
        Image.open(image).close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form['text']
    generate_pdf(data)
    return send_file('output.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
