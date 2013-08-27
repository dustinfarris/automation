def choose(question, choices):
    """Ask user to choose from a list of enumerated choices."""
    print("\n%s\n" % question)
    for number, choice in enumerate(choices, start=1):
        print("  %d) %s" % (number, str(choice)))
    user_choice = input("\n> ")
    return choices[int(user_choice) - 1]
