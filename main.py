from quiz_game import QuizGame
import os

def clear_screen():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Exibe o menu principal"""
    print("🎯 QUIZ TRIVIA 🎯")
    print("=" * 30)
    print("1. Iniciar Novo Jogo")
    print("2. Ver Categorias")
    print("3. Sair")
    print("=" * 30)

def get_difficulty():
    """Obtém a dificuldade escolhida pelo usuário"""
    print("\n🎚️  SELECIONE A DIFICULDADE:")
    print("1. Fácil")
    print("2. Médio") 
    print("3. Difícil")
    print("4. Qualquer")
    
    while True:
        choice = input("\nEscolha (1-4): ").strip()
        if choice == '1':
            return 'easy'
        elif choice == '2':
            return 'medium'
        elif choice == '3':
            return 'hard'
        elif choice == '4':
            return 'any'
        else:
            print("Opção inválida! Tente novamente.")

def get_question_type():
    """Obtém o tipo de questão"""
    print("\n📝 SELECIONE O TIPO DE QUESTÃO:")
    print("1. Múltipla Escolha")
    print("2. Verdadeiro ou Falso")
    print("3. Qualquer")
    
    while True:
        choice = input("\nEscolha (1-3): ").strip()
        if choice == '1':
            return 'multiple'
        elif choice == '2':
            return 'boolean'
        elif choice == '3':
            return 'any'
        else:
            print("Opção inválida! Tente novamente.")

def get_number_of_questions():
    """Obtém o número de questões"""
    while True:
        try:
            num = int(input("\nQuantas questões? (mínimo 5): "))
            if num >= 5:
                return num
            else:
                print("Mínimo de 5 questões!")
        except ValueError:
            print("Por favor, digite um número válido!")

def play_game(quiz: QuizGame):
    """Executa o jogo principal"""
    clear_screen()
    
    # Configurações do jogo
    categories = quiz.get_categories()
    
    print("📚 CATEGORIAS DISPONÍVEIS:")
    for id, name in categories.items():
        print(f"{id}: {name}")
    
    try:
        category_id = int(input("\nDigite o ID da categoria (ou 0 para qualquer): "))
        category = category_id if category_id != 0 else None
    except:
        category = None
    
    difficulty = get_difficulty()
    question_type = get_question_type()
    num_questions = get_number_of_questions()
    
    # Buscar questões
    print("\n🎲 Buscando questões...")
    if not quiz.fetch_questions(num_questions, category, difficulty, question_type):
        return
    
    clear_screen()
    print("🎯 QUIZ INICIADO! 🎯")
    print("=" * 40)
    
    # Loop das questões
    while True:
        question_data = quiz.get_current_question()
        if not question_data:
            break
        
        current, total = quiz.get_progress()
        
        print(f"\n📊 Progresso: {current}/{total}")
        print(f"🎯 Pontuação: {quiz.score}")
        print(f"📖 Categoria: {question_data['category']}")
        print(f"⚡ Dificuldade: {question_data['difficulty'].title()}")
        print(f"\n❓ {question_data['question']}")
        print("\n📝 Opções:")
        
        for i, answer in enumerate(question_data['answers'], 1):
            print(f"   {i}. {answer}")
        
        # Obter resposta do usuário
        while True:
            try:
                choice = int(input(f"\nSua resposta (1-{len(question_data['answers'])}): "))
                if 1 <= choice <= len(question_data['answers']):
                    user_answer = question_data['answers'][choice - 1]
                    break
                else:
                    print(f"Por favor, digite um número entre 1 e {len(question_data['answers'])}")
            except ValueError:
                print("Por favor, digite um número válido!")
        
        # Verificar resposta
        if quiz.check_answer(user_answer):
            print("\n✅ Resposta Correta!")
        else:
            print(f"\n❌ Resposta Incorreta!")
            print(f"💡 A resposta correta era: {question_data['correct_answer']}")
        
        input("\nPressione Enter para continuar...")
        clear_screen()
        
        # Próxima questão
        if not quiz.next_question():
            break
    
    # Resultado final
    score, total = quiz.get_score()
    percentage = (score / total) * 100
    
    print("🎊 FIM DO JOGO! 🎊")
    print("=" * 30)
    print(f"📊 Pontuação Final: {score}/{total}")
    print(f"📈 Percentual de Acertos: {percentage:.1f}%")
    
    if percentage >= 80:
        print("🏆 Excelente! Você é um mestre do trivia!")
    elif percentage >= 60:
        print("👍 Muito bom! Continue praticando!")
    elif percentage >= 40:
        print("😊 Bom trabalho! Há espaço para melhorar!")
    else:
        print("💪 Não desanime! Tente novamente!")
    
    input("\nPressione Enter para voltar ao menu...")

def main():
    """Função principal"""
    quiz = QuizGame()
    
    while True:
        clear_screen()
        display_menu()
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == '1':
            play_game(quiz)
        elif choice == '2':
            clear_screen()
            print("📚 CATEGORIAS DISPONÍVEIS:")
            print("=" * 30)
            categories = quiz.get_categories()
            for id, name in categories.items():
                print(f"{id}: {name}")
            input("\nPressione Enter para voltar...")
        elif choice == '3':
            print("\nObrigado por jogar! Até mais! 👋")
            break
        else:
            print("Opção inválida! Tente novamente.")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main()
