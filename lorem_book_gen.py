import re, random
from nltk.tokenize import SyllableTokenizer

seed_text = "Sed ut perspiciatis, unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam eaque ipsa, \
quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt, explicabo. Nemo enim ipsam voluptatem, quia voluptas sit, aspernatur \
aut odit aut fugit, sed quia consequuntur magni dolores eos, qui ratione voluptatem sequi nesciunt, neque porro quisquam est, qui dolorem ipsum, \
quia dolor sit amet consectetur adipisci[ng] velit, sed quia non numquam [do] eius modi tempora inci[di]dunt, ut labore et dolore magnam aliquam quaerat voluptatem. \
Ut enim ad minima veniam quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure \
reprehenderit, qui in ea voluptate velit esse, quam nihil molestiae consequatur, vel illum, qui dolorem eum fugiat, quo voluptas nulla pariatur? \
At vero eos et accusamus et iusto odio dignissimos ducimus, qui blanditiis praesentium voluptatum deleniti atque corrupti, quos dolores et \
quas molestias excepturi sint, obcaecati cupiditate non provident, similique sunt in culpa, qui officia deserunt mollitia animi, id est laborum et dolorum fuga. \
Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio, cumque nihil impedit, quo minus id, quod \
maxime placeat, facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus \
saepe eveniet, ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores \
alias consequatur aut perferendis doloribus asperiores repellat…"

word_pool = [re.compile('[^a-zA-Z]').sub('', word).lower() for word in seed_text.split()]

def generate_paragraph(num_words=50, end_punc='.'):

    words = random.sample(word_pool, num_words)
    puncs = ["?", "!", ".", ",", ",", ",", ",", ","]
    break_points = set()

    num_breakpoints = random.randint(num_words//10, num_words//5)

    while len(break_points) < num_breakpoints:
        break_idx = random.randint(0, num_words-2)
        if not (break_idx + 1 in break_points or break_idx-1 in break_points):
            break_points.add(break_idx)

    for idx in break_points:
        words[idx] = words[idx] + random.choice(puncs)
        if words[idx][-1] != ",":
            words[idx+1] = words[idx+1].title()

    words[-1] = words[-1] + end_punc
    words[0] = words[0][0].upper() + words[0][1:]

    return " ".join(words)

def generate_free_poem(min_lines=5, max_lines=20, max_indent_size=12, max_line_len=5):
    num_lines = random.randint(min_lines, max_lines)
    start = "Lorem ipsum dolor sit amet consectetur adipiscing elit".split()
    start[0] = " "*random.randint(0, max_indent_size//2) + start[0]
    for i in range(1, len(start)):
        if random.uniform(0,1) > 0.7:
            start[i] = "\n" + " "*random.randint(0, max_indent_size) + start[i]

    text = " ".join(start) + " "

    for _ in range(num_lines):
        text += "\n" + " "*random.randint(0, max_indent_size) + " ".join(random.sample(word_pool, random.randint(1, max_line_len)))
    
    return text

def generate_letter():
    p1, p2, p3 = [generate_paragraph(random.randint(20, 60)) for _ in range(3)]
    return f"Lorem Ipsum,\n\nDolor sit amet, consectetur adipiscing elit. {p1}\n\n{p2}\n\n{p3}\n\nUrna Semper"

def generate_news_article():
    text = "\033[1m" + "'Lorem ipsum dolor sit amet': consectetur adipiscing elit" + "\033[0m" + "\nUrna Semper\n\n"

    for _ in range(8):
        text += "    " + generate_paragraph(random.randint(10, 60)) + "\n"

    return text + "\n\nNam liber aliquam..."

def generate_haiku_line(syllables):
    SSP, line_len, line = SyllableTokenizer(), 0, []
    while line_len != syllables:
        word = random.choice(word_pool)
        word_len = len(SSP.tokenize(word))
        if syllables - line_len >= word_len:
            line.append(word)
            line_len += word_len
    line[0] = line[0].title()
    return " ".join(line)

def generate_haiku():
    return generate_haiku_line(5) +  "\n" + generate_haiku_line(7) + "\n" + generate_haiku_line(5)

def generate_qna():
    text = ""
    for _ in range(5):
        text += "\x1B[3m" + generate_paragraph(random.randint(6, 30), '?') + "\x1B[0m\n" + generate_paragraph(random.randint(20, 50)) + "\n\n"
    return text

def generate_word_cloud_corpus(): # Used wordclouds.com to generate word cloud
    return generate_paragraph(200)

print(generate_letter() + "\n\n" + generate_free_poem() + "\n\n" + generate_news_article() + "\n\n" + generate_haiku() + "\n\n" + generate_word_cloud_corpus())