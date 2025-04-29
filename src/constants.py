alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
small_letter_color = "#0000FF"
big_letter_color = "#FF0000"

difficulty_levels = {
    "easy": {
        "level": 0,
        "computer_tank_speed": 110,
        "letter_cost": 5,
        "medicine_cost":{
            "wall": 1,
            "radar": 2,
            "air_defence": 5,
        },
        "movable_wall_cost": 10,
        "air_defence_rocket_cost": 12,
        "missing_letters_counter": 5,
        "win_points": 200
    },
    "medium": {
        "level": 1,
        "computer_tank_speed": 90,
            "letter_cost": 3,
            "medicine_cost":{
                "wall": 3,
                "radar": 5,
                "air_defence": 10,
            },
            "movable_wall_cost": 15,
            "air_defence_rocket_cost": 18,
            "missing_letters_counter": 3,
            "win_points": 300
    },
    "hard": {
        "level": 2,
        "computer_tank_speed": 60,
            "letter_cost": 2,
            "medicine_cost":{
                "wall": 5,
                "radar": 10,
                "air_defence": 20,
            },
            "movable_wall_cost": 50,
            "air_defence_rocket_cost": 60,
            "missing_letters_counter": 1,
            "win_points": 500
    }
}