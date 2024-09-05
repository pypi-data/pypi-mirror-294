import random
from load_and_preprocess_data import load_and_preprocess_data
from genrator import genrate_response
from rouge import Rouge
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize ROUGE evaluator
rouge = Rouge()

# Load the data
df = load_and_preprocess_data()

def create_prompt(examples, query):
    prompt = "You are provided with examples of content followed by their corresponding reasons summarized in a few words, comma-separated. Please summarize the new content similarly.\n\n"
    i = 0
    for index, row in examples.iterrows():
        prompt += f"{i}. Content: {row['Content']}\n"
        prompt += f"{i}. Summary of Claim: {row['Reasons']}\n\n"
        i += 1
    
    prompt += "Now, summarize the following content:\n"
    prompt += f"Content: {query}\n"
    prompt += "Just Output the Summary of the Claim as a string and nothing else\n"
    
    return prompt

def perfomance_on_data():

    # Initialize accumulators for ROUGE and Cosine scores
    total_rouge_1 = 0
    total_rouge_2 = 0
    total_rouge_l = 0
    total_cosine = 0
    num_examples = 0

    # Iterate over the dataset
    for query, reason in zip(df['Content'], df['Reasons']):
        examples = df.sample(7)
        prompt = create_prompt(examples, query)
        try:
            response = genrate_response(prompt)
            generated_summary = response.text

            # Calculate ROUGE score
            rouge_scores = rouge.get_scores(generated_summary, reason, avg=True)
            total_rouge_1 += rouge_scores['rouge-1']['f']
            total_rouge_2 += rouge_scores['rouge-2']['f']
            total_rouge_l += rouge_scores['rouge-l']['f']

            # Calculate Cosine Similarity
            vectorizer = TfidfVectorizer().fit_transform([generated_summary, reason])
            vectors = vectorizer.toarray()
            cosine_sim = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
            total_cosine += cosine_sim

            num_examples += 1
            print(response.text)
            print(generated_summary)
            print(reason)
            print(rouge_scores)
            print(cosine_sim)

        except Exception as error:
            print("Something went wrong:", error)
        print("=====================================")

    # Compute average scores
    if num_examples > 0:
        avg_rouge_1 = total_rouge_1 / num_examples
        avg_rouge_2 = total_rouge_2 / num_examples
        avg_rouge_l = total_rouge_l / num_examples
        avg_cosine = total_cosine / num_examples

        print(f"Average ROUGE-1 F1 Score: {avg_rouge_1}")
        print(f"Average ROUGE-2 F1 Score: {avg_rouge_2}")
        print(f"Average ROUGE-L F1 Score: {avg_rouge_l}")
        print(f"Average Cosine Similarity: {avg_cosine}")
    else:
        print("No valid examples were processed.")


def genrate_on_query():
    print("Enter the Content")
    query = input()
    examples = df.sample(7)
    prompt = create_prompt(examples, query)
    try:
        print("Summary of Claims ")
        response = genrate_response(prompt)
        print(response.text)
    except Exception as error:
        print("Something went wrong:", error)
