import requests
import html
from typing import List, Dict, Any
from translator import Translator

class QuizGame:
    def __init__(self):
        self.base_url = "https://opentdb.com/api.php"
        self.translator = Translator()
        self.score = 0
        self.total_questions = 0
        self.current_question = 0
        self.questions = []
    
    def get_categories(self) -> Dict[int, str]:
        """Obtém as categorias disponíveis"""
        try:
            response = requests.get("https://opentdb.com/api_category.php")
            data = response.json()
            categories = {cat['id']: cat['name'] for cat in data['trivia_categories']}
            return categories
        except:
            # Categorias padrão caso a API falhe
            return {
                9: "General Knowledge",
                10: "Books",
                11: "Film",
                12: "Music",
                13: "Musicals & Theatres",
                14: "Television",
                15: "Video Games",
                16: "Board Games",
                17: "Science & Nature",
                18: "Computers",
                19: "Mathematics",
                20: "Mythology",
                21: "Sports",
                22: "Geography",
                23: "History",
                24: "Politics",
                25: "Art",
                26: "Celebrities",
                27: "Animals",
                28: "Vehicles",
                29: "Comics",
                30: "Gadgets",
                31: "Japanese Anime & Manga",
                32: "Cartoon & Animations"
            }
    
    def fetch_questions(self, amount: int = 5, category: int = None, 
                       difficulty: str = None, question_type: str = None) -> bool:
        """Busca questões da API"""
        params = {
            'amount': amount,
            'encode': 'url3986'
        }
        
        if category:
            params['category'] = category
        if difficulty and difficulty != 'any':
            params['difficulty'] = difficulty
        if question_type and question_type != 'any':
            params['type'] = question_type
        
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if data['response_code'] == 0:
                self.questions = data['results']
                self.total_questions = len(self.questions)
                self.current_question = 0
                self.score = 0
                return True
            else:
                print("Erro ao buscar questões. Tente novamente.")
                return False
                
        except Exception as e:
            print(f"Erro na conexão: {e}")
            return False
    
    def decode_text(self, text: str) -> str:
        """Decodifica texto da API"""
        return html.unescape(text)
    
    def get_current_question(self) -> Dict[str, Any]:
        """Retorna a questão atual com opções traduzidas"""
        if self.current_question >= self.total_questions:
            return None
        
        question_data = self.questions[self.current_question]
        
        # Decodificar texto
        question = self.decode_text(question_data['question'])
        correct_answer = self.decode_text(question_data['correct_answer'])
        incorrect_answers = [self.decode_text(ans) for ans in question_data['incorrect_answers']]
        
        # Traduzir para português
        question_pt = self.translator.translate(question)
        correct_answer_pt = self.translator.translate(correct_answer)
        incorrect_answers_pt = [self.translator.translate(ans) for ans in incorrect_answers]
        
        # Combinar todas as respostas
        all_answers = incorrect_answers_pt + [correct_answer_pt]
        
        # Embaralhar respostas
        import random
        random.shuffle(all_answers)
        
        return {
            'question': question_pt,
            'answers': all_answers,
            'correct_answer': correct_answer_pt,
            'category': question_data['category'],
            'difficulty': question_data['difficulty'],
            'type': question_data['type']
        }
    
    def check_answer(self, user_answer: str) -> bool:
        """Verifica se a resposta está correta"""
        current_q = self.get_current_question()
        if current_q and user_answer == current_q['correct_answer']:
            self.score += 1
            return True
        return False
    
    def next_question(self) -> bool:
        """Avança para a próxima questão"""
        self.current_question += 1
        return self.current_question < self.total_questions
    
    def get_score(self) -> tuple:
        """Retorna pontuação atual"""
        return self.score, self.total_questions
    
    def get_progress(self) -> tuple:
        """Retorna progresso atual"""
        return self.current_question + 1, self.total_questions
