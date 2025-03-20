import re
import nltk
import csv
import matplotlib.pyplot as plt
from collections import Counter
from nltk.corpus import stopwords

# Download required NLTK resources (only needed once)
nltk.download('punkt')
nltk.download('stopwords')


def process_text_file(filename):
    """Process a text file to analyze word frequencies and extract sentences."""

    # Read the input file
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()

    # Tokenize text into sentences
    sentences = nltk.sent_tokenize(text)

    # Tokenize text into words
    words = nltk.word_tokenize(text)

    # Convert to lowercase and remove non-alphabetic tokens
    words = [word.lower() for word in words if word.isalpha()]

    # Get English stopwords
    stop_words = set(stopwords.words('english'))

    # Add names and other custom stopwords
    custom_stopwords = {
        'monica', 'chandler', 'joey', 'richard', 'phoebe', 'ross', 'rachel',
        'thompson', 'elizabeth', 'n\'t', 's', 're', 'm', 'na', 'gon',
        # Add more names or postfix words as needed
    }

    # Combine all stopwords
    all_stopwords = stop_words.union(custom_stopwords)

    # Filter out stopwords
    filtered_words = [word for word in words if word not in all_stopwords]

    # Save tokens to file
    with open('w_tokens.txt', 'w', encoding='utf-8') as f:
        for word in filtered_words:
            f.write(f"{word}\n")

    # Create a bag of words (word frequency)
    word_counts = Counter(filtered_words)
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    # Save the entire BoW to CSV
    with open('BoW.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for word, count in sorted_word_counts:
            writer.writerow([word, count])

    # Get the top 20 most frequent words
    top_20_words = [word for word, count in sorted_word_counts[:20]]

    # Plot the 20 most frequently used words
    plt.figure(figsize=(12, 6))
    plt.bar([word for word, _ in sorted_word_counts[:20]], [count for _, count in sorted_word_counts[:20]])
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Top 20 Most Frequent Words')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('top_20_words.png')
    plt.show()

    # Extract sentences containing the top 20 words
    sentences_with_top20 = []
    for sentence in sentences:
        # Check if any of the top 20 words are in the sentence
        if any(re.search(r'\b' + re.escape(word) + r'\b', sentence.lower()) for word in top_20_words):
            sentences_with_top20.append(sentence)

    # Save sentences with top 20 words
    with open('sentences_with_top20.txt', 'w', encoding='utf-8') as f:
        f.write('\n' + '-' * 50 + '\n'.join(sentences_with_top20))

    # Also save all sentences for comparison
    with open('all_sentences.txt', 'w', encoding='utf-8') as f:
        f.write('\n' + '-' * 50 + '\n'.join(sentences))

    return top_20_words, word_counts


if __name__ == "__main__":
    # Specify the input text file
    input_file = "friends_ep624.txt"  # Replace with your file

    print(f"Processing file: {input_file}")
    top_words, word_counts = process_text_file(input_file)

    print("\nTop 20 most frequent words:")
    for i, word in enumerate(top_words, 1):
        print(f"{i}. {word}: {word_counts[word]} occurrences")

    print("\nProcessing complete. Files created:")
    print("- w_tokens.txt (tokenized words)")
    print("- BoW.csv (bag of words with frequencies)")
    print("- top_20_words.png (bar chart of top 20 words)")
    print("- sentences_with_top20.txt (sentences containing top 20 words)")
    print("- all_sentences.txt (all sentences for comparison)")