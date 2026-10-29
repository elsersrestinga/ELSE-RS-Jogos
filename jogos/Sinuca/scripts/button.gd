extends Button

@export var _game_state: GameState


func _ready():
	var button = Button.new()
	button.text = "Restart"
	button.pressed.connect(_button_pressed)
	add_child(button)

func _button_pressed():
	get_tree().reload_current_scene()
	_game_state.balls_remaining_by_player_id = [7, 7]
	_game_state.current_player_id = 0
	_game_state.ball_suit_by_player_id = [Enums.BallType.TBD, Enums.BallType.TBD]
	_game_state.current_play_state = Enums.PlayState.BALL_IN_HAND
