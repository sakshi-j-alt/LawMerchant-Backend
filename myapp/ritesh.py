
from .models import regu_connection
import spacy

# Load the spaCy large model
nlp = spacy.load('en_core_web_lg')

# Define the keywords related to the product
# keywords = ['turmeric','dahi','milk','regulation']

# Function to extract relevant sentences
def extract_relevant_sentences(doc, keywords):
    relevant_sentences = []
    for sentence in doc.sents:
        if any(keyword.lower() in sentence.text.lower() for keyword in keywords):
            relevant_sentences.append(sentence.text)
    return relevant_sentences

def extract_relevant_sentences1(doc, keywords):
    relevant_sentences = []
    for sentence in doc.sents:
        if all(keyword.lower() in sentence.text.lower() for keyword in keywords):
            relevant_sentences.append(sentence.text)
    return relevant_sentences

def extract_relevant_sentences2(doc, keywords):
    relevant_sentences = []
    for sentence in doc.sents:
        keyword_count = sum(1 for keyword in keywords if keyword.lower() in sentence.text.lower())
        if keyword_count > 1:
            relevant_sentences.append(sentence.text)
    return relevant_sentences

# Sample document text
text = """Regulations: General principals

1. Approval of Article of Food and Label:
Regulation: Approval of Article of Food and Label
	a)Must be approved by the Food Authority before manufacture, sale, or storage.

2. Packaging:
Regulation: Packaging
	a) Be packed in hermetically sealed, clean, and sound containers.
	b)Use flexible packs made from paper, polymer, and/or metallic film as per Food Safety and Standards (Packaging) Regulations 2018.
	c)Protect contents from deterioration.
	d)Be packed under an inert atmosphere.
	e)Use packaging material free from Bisphenol A (BPA).

3. Nutrient Declaration:
Regulation: Nutrient Declaration
	a)Allows a variation of minus 10.0 percent from declared value.
	b)Nutrient levels must not exceed the maximum limits specified in the composition tables.

4. Source Compounds for Nutrients:
Regulation: Source Compounds for Nutrients
	a)Minerals, vitamins, and other nutrients as per Schedule-I(a), Schedule-I(b), and Schedule-I(c).

5. DHA and ARA Content:
Regulation: DHA and ARA Content
	a)Contain algal and fungal oil sources of DHA and ARA from Crypthecodinium cohnii, Mortierella alpina, Schizochytrium sp., Ulkenia sp., or fish oil.
	b)DHA level must be a maximum of 0.5 percent of total fatty acids.
	c)Maintain ARA ratio of at least 1:1.

6. Carbohydrate Source:
Regulation: Carbohydrate Source
	a)Lactose and glucose polymers.
	b)Sucrose and/or fructose only if needed, and not exceeding 20 percent of total carbohydrate.

7. Product Quality:
Regulation: Product Quality
	a)Be free from lumps and coarse particles.
	b)Be uniform in appearance.
	c)Be free from rancid taste and musty odour.

8. Compliance with Acts:
Regulation: Compliance with Acts
	a)Infant Milk Substitutes, Feeding Bottles, and Infant Foods (Regulation of Production, Supply, and Distribution) Act 1992 (42 of 1992) as amended in 2003.
	b)Advertisement, marketing, and promotion aspects.

9. Legal Metrology Compliance:
Regulation: Legal Metrology Compliance
	a)Legal Metrology (Packaged Commodities) Rules 2011.

10. Contaminants and Residues Compliance:
Regulation: Contaminants and Residues Compliance
	a)Food Safety and Standards (Contaminants, Toxins, and Residues) Regulations 2011.

11. Prohibition and Restriction of Sales Compliance:
Regulation: Prohibition and Restriction of Sales Compliance
	a)Food Safety and Standards (Prohibition and Restriction of Sales) Regulation 2011.

12. Microbiological Requirements:
Regulation: Microbiological Requirements
	a)Microbiological requirements specified under Appendix B of Food Safety and Standards (Food Products Standards and Food Additives) Regulations 2011.

13. Advertising and Claims:
Regulation: Advertising and Claims
	a)Be in accordance with the Food Safety and Standards (Advertising and Claims) Regulations 2018.

14. Nutritional Composition Compliance:
Regulation: Nutritional Composition Compliance
	a)Comply with the nutritional composition specified on a 100 gm or 100 kcal basis under specific product categories in the composition tables.



--------------------
Regulation: Labelling Requirements for Foods for Infant Nutrition

1. General Labelling:
Regulation: General Labelling
	a)Food Safety and Standards (Labelling and Display) Regulations 2020.
	b)Specific labelling requirements provided under these regulations.

2. Important Notice:
Regulation: Important Notice
	a)The words "IMPORTANT NOTICE" in capital letters.
	b)A statement "MOTHER’S MILK IS BEST FOR YOUR BABY" in capital letters, with text not less than five millimeters in height, printed on the front of the pack.
	c)For infant food: A statement indicating "Infant food shall be introduced only after the age of six months and up to the age of two years."
	d)For food for special medical purposes: The statement "MOTHER’S MILK IS BEST FOR YOUR BABY" is not required if breastfeeding is contraindicated.

3. Usage Advice:
Regulation: Usage Advice
	a)Infant milk substitute or infant food should be used only on the advice of a health worker.

4. Warning:
Regulation: Warning
	a)Infant milk substitute or infant food is not the sole source of nourishment for an infant.

5. Preparation Instructions:
Regulation: Preparation Instructions
	a)Instructions for appropriate and hygienic preparation.
	b)Cleaning of utensils, bottles, and teats.
	c)Warning against health hazards of inappropriate preparations.

6. Nutrient Composition:
Regulation: Nutrient Composition
	a)Energy value in kilocalories or kilojoules.

7. Storage Conditions:
Regulation: Storage Conditions
	a)"Store in a cool and dry place in an airtight container."

8. Feeding Instructions:
Regulation: Feeding Instructions
	a)Feeding chart.
	b)Directions for use, including instructions for discarding leftover feed.

9. Measuring Scoop Instructions:
Regulation: Measuring Scoop Instructions
	a)Use of the measuring scoop (level or heaped).
	b)Quantity per scoop.

10. Batch Details:
Regulation: Batch Details
	a)Batch number.
	b)Month and year of manufacture.
	c)Use by date, Recommended Last Consumption date, or Expiry Date.

11. Protein Efficiency Ratio:
Regulation: Protein Efficiency Ratio
	a) A minimum protein efficiency ratio (PER) of 2.5.

12. Additives Declaration:
	a)Regulation: Additives Declaration
	b)The specific name of food additives and appropriate class titles if permitted.

13. Prohibited Graphics:
Regulation: Prohibited Graphics
	a)Pictures of infants or women, or other graphics designed to increase saleability.
	b)Terms like “Humanised” or “Maternalised.”
	c)Words like “Full Protein Food” or “Health Food.”

14. Milk Declaration:
Regulation: Milk Declaration
	a)“Contains no milk or milk products or milk derivatives.”

15. Surrounding Line for Warnings:
Regulation: Surrounding Line for Warnings
	a)“unsuitable for babies” are required to be used.

16. Allergen Warning:
Regulation: Allergen Warning
	a)Any ingredients with known allergenicity are present.

17. Contamination Warning:
Regulation: Contamination Warning
	a)Imported ingredients.

------------------------
Regulation: Infant Formula
	a)Infant formula shall be in powder form and conform to the nutritional composition in Schedule-I (1).
	b)It shall be based on milk or mixtures of milk and other ingredients.
	c)The protein efficiency ratio (PER) shall be a minimum of 2.5.
	d)The source of protein shall be either milk protein or mixtures of milk protein and protein from cereals or legumes, provided the protein efficiency ratio (PER) is met.

Regulation: Follow-up Formula
	a)Follow-up formula shall be in powder form and conform to the nutritional composition in Schedule-I (2).
	b)It shall be based on milk, cereal, soy protein isolates, or a mixture of these ingredients.
	c)The protein efficiency ratio (PER) shall be a minimum of 2.5.
	d)It shall provide energy, protein, fat, carbohydrates, vitamins, and minerals in the specified quantities.

Regulation: Milk Cereal Based Complementary Food
	a)Milk cereal based complementary food shall be in powder form.
	b)It shall provide the specified quantities of nutrients as per Schedule-I (3).
	c)It shall be made from milk, cereals, legumes, millets, nuts, and protein concentrates or isolates.

Regulation: Processed Cereal Based Complementary Food
	a)Processed cereal based complementary food shall be in powder form.
	b)It shall provide the specified quantities of nutrients as per Schedule-I (4).
	c)It shall be made from cereals, legumes, millets, nuts, and protein isolates or concentrates.

Regulation: Food for Special Medical Purposes
	a)Food for special medical purposes intended for infants shall meet the specific nutritional requirements of infants with specific disorders, diseases, or medical conditions.
	b)It shall be manufactured under medical supervision and conform to the nutritional composition in Schedule-I (5).

--------------------------------
Regulation: Nutritional Composition Details 

a)Infant Formula (Schedule-I (1)):
	i)Protein: Minimum 1.8 g/100 kcal, Maximum 3.0 g/100 kcal
	ii)Fat: Minimum 3.0 g/100 kcal, Maximum 6.0 g/100 kcal
	iii)Linoleic Acid: Minimum 300 mg/100 kcal, Maximum 1200 mg/100 kcal
	iv)Vitamins & Minerals: Additional detailed nutrient values and limits as specified in the regulation.
b)Follow-up Formula (Schedule-I (2)):
	i)Protein: Minimum 3.0 g/100 kcal, Maximum 4.5 g/100 kcal
	ii)Fat: Minimum 3.0 g/100 kcal, Maximum 6.0 g/100 kcal
	iii)Linoleic Acid: Minimum 300 mg/100 kcal, Maximum 1200 mg/100 kcal
	iv)Vitamins & Minerals: Additional detailed nutrient values and limits as specified in the regulation.
c)Milk Cereal Based Complementary Food (Schedule-I (3)):
	i)Protein: Minimum 3.0 g/100 kcal, Maximum 4.5 g/100 kcal
	ii)Fat: Minimum 3.0 g/100 kcal, Maximum 6.0 g/100 kcal
	iii)Linoleic Acid: Minimum 300 mg/100 kcal, Maximum 1200 mg/100 kcal
	iv)Vitamins & Minerals: Additional detailed nutrient values and limits as specified in the regulation.
d)Processed Cereal Based Complementary Food (Schedule-I (4)):
	i)Protein: Minimum 3.0 g/100 kcal, Maximum 4.5 g/100 kcal
	ii)Fat: Minimum 3.0 g/100 kcal, Maximum 6.0 g/100 kcal
	iii)Linoleic Acid: Minimum 300 mg/100 kcal, Maximum 1200 mg/100 kcal
	iv)Vitamins & Minerals: Additional detailed nutrient values and limits as specified in the regulation.
e)Food for Special Medical Purposes (Schedule-I (5)):
	i)Protein: Minimum 3.0 g/100 kcal, Maximum 4.5 g/100 kcal
	ii)Fat: Minimum 3.0 g/100 kcal, Maximum 6.0 g/100 kcal
	iii)Linoleic Acid: Minimum 300 mg/100 kcal, Maximum 1200 mg/100 kcal
	iv)Vitamins & Minerals: Additional detailed nutrient values and limits as specified in the regulation.
"""
def processData(keywords) :
    # Process the document
    doc = nlp(text)

    # Extract relevant sentences
    relevant_sentences = extract_relevant_sentences2(doc, keywords)
    return relevant_sentences


