

# Example usage (French data):
from manifactor import create_math_club_pdf, create_math_club_program


data = {
    'school_name': "Lycée qualifiant Ziraoui",
    'date': "18/02/2025",
    'attendance': [
        ["P. Mohamed OUALIL", "Coordinateur du club"],
        ["ELMOUSSAOUI Nohaila", "Élève"],
        ["AIT ABDELLAH ABIR", "Élève"],
        ["ZOUANE SOUFIANE", "Élève"],
        ["CHIDMI Yassine", "Élève"],
        ["HOUZIR Rachida", "Élève"],
        ["QASSAM Yasmine", "Élève"],
        ["SALMAN Zineb", "Élève"],
        ["MAJID Youssef", "Élève"],
        ["HAMMOU AICHA", "Élève"],
        ["NOUJ Lina", "Élève"],
        ["ECHAYB ABRAR", "Élève"],
        ["AMCHTKOU Fatima Ezzahra", "Élève"],
    ],
    'agenda': [
        "Encourager la progression des élèves les plus talentueux",
        "Accompagner les élèves à haut potentiel dans leur apprentissage",
        "Explorer des problèmes mathématiques complexes et originaux",
        "Apprendre des techniques de résolution de problèmes",
        "Maîtriser des stratégies efficaces en mathématiques",
        "Développer la pensée logique et critique",
        "Améliorer la communication mathématique",
        "Favoriser l'autonomie et la confiance en soi",
        "Susciter la curiosité et l'envie d'apprendre",
    ],
    # ... add other data ...
}

create_math_club_pdf("math_club_record_fr.pdf", data)
print("PDF created successfully!")


# Example Data
data = {
    'titles': [
        'Programme des Activités du Club de Mathématiques',
        'Année scolaire 2024/2025'
    ],
    'introduction': "Le club de mathématiques est heureux de dévoiler son programme d'activités pour l'année. Nous avons conçu un programme stimulant et varié, qui permettra aux membres de développer leurs compétences et leur passion pour les mathématiques.",
    'activities': [
        {
            'title': "Olympiad des mathématiques",
            'description': "Activités programmés pour les trois niveaux collégiaux scolaires .",
            'details': [
                "Période: 2ème semestre",
                "3APIC: Mener à bien des dernières étapes de la compétition, discuter les résultats et passer d'autres preuves.",
                "1APIC et 2APIC : Organiser des premières étapes de la compétition",
                "Pour tous les niveaux : préparer les élèves pour les années à venir"
            ]
        },
        {
            'title': "Ateliers des Mathématiques",
            'description': "Organiser des séances fréquentes pour réaliser les objectifs soulignés pour le club .",
            'details': [
                "Période: 2ème semestre",
                "Niveau: 3APIC",
                "Duréé : 2h par séance",
            ]
        },
        {
            'title': "exposés",
            'description': "Présenter des exposés pour les niveaux collègiaux .",
            'details': [
                "Période: 2ème semestre",
                "Exposé 1 : La révision des cours",
                "Exposé 2 : Comprendre le succés",
                "Exposé 3 : L'importance des mathématiques",
            ]
        },
        # ... more activities
    ]
}

create_math_club_program("math_club_program.pdf", data)
print("PDF created successfully!")
