from xml.etree import ElementTree
import gensim, string, collections, os, re

# Arguments: Directory of XML src files, Article Year, < ArticleCategories>
def emb_builder(src_dir, year_min , year_max, category_0 = "", category_1 = "", category_2 = ""):
    parsed_txt = []

    # Iterate through files in directory
    for root, dirs, files in os.walk(src_dir):
        for folder in dirs:
            dirpath = (os.path.join(src_dir, folder))
            for root, dirs, files in os.walk(dirpath):
                for fname in files:
                    filepath = (os.path.join(dirpath, fname))

                    with open(filepath) as f:
                        article = ElementTree.parse(f)
                    parsed = False

                    # Check if article is in the desired category & from correct publication year
                    for node in article.findall('.//classifier'):
                        article_yr = (int)((article.find('.//doc.copyright')).attrib.get('year'))
                        article_ctg = "NONE"
                        if ("general_descriptor" == node.attrib.get('type')):
                            article_ctg = node.text

                        # Find body content from XML and Preprocess text
                        # Add to raw_txt arrray
                        if (parsed == False and year_max >= article_yr and year_min <= article_yr and\
                        (article_ctg == category_0 or article_ctg == category_1 or article_ctg == category_2)):
                            for node in article.findall('.//block'):
                                parsed = True
                                block_type = node.attrib.get('class')
                                if block_type == 'full_text':
                                    for p in node.findall('.//p'):
                                        p_text = re.sub("[\'\.\t\,\:;\(\)\.]", "",p.text, 0, 0)
                                    parsed_txt.append(p_text.lower().split())

    # Run Word2Vec on preprocessed text
    word_emb  = gensim.models.Word2Vec(parsed_txt, min_count = 1)
    word_emb.save("Election_finance")
    vocab = list(word_emb.vocab.keys())

    print word_emb
    print (vocab)
    print word_emb.similarity("secretary", "government")

emb_builder("/home/jaredfern/Desktop/LDC_01/", 2000, 2007, "Finances", "Politics and Government", "Elections")
