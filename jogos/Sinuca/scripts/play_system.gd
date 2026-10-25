extends Node3D

@export var _cue_ball: Ball
@export var _aim_container: Node3D
@export var _cue_stick: Node3D
@export var _stick_animation_player: AnimationPlayer
@export var _aim_cam: Camera3D
@export var _game_state: GameState

@export var _stick_min_z := 0.75
@export var _stick_max_z := 1.4
@export var _stick_z_sens := 0.02
@export var _shot_power_min:= 0.1
@export var _shot_power_max:= 5.0

var _shot_percent : float = 0
# finite state machine
#var _play_state: Enums.PlayState = Enums.PlayState.AIMING

func _ready():
	#Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	GameEvents.shot_completed.connect(_setup_next_shot)
	_cue_ball.position = BilliardTable.HEAD_SPOT
	
	
func _process(_delta):
	_handle_shot_input()

	_aim_container.position = _cue_ball.position
	
#	_process_cheat_mode()
	
func _input(event):
	var mouse_motion = event as InputEventMouseMotion
	if mouse_motion:
		_aim_container.rotation_degrees.y += mouse_motion.relative.x
	
	if Input.is_action_just_pressed("mover_taco_tras"):
		_shot_percent += _stick_z_sens
	if Input.is_action_just_pressed("mover_taco_frente"):
		_shot_percent -= _stick_z_sens
	
		#_shot_percent += mouse_motion.relative.y * _stick_z_sens
	_shot_percent = clamp(_shot_percent, 0, 1)
	_cue_stick.position.z = lerp(_stick_min_z, _stick_max_z, _shot_percent)
		
		#_cue_stick.position.z += mouse_motion.relative.y * _stick_z_sens
		#_cue_stick.position.z = clamp(_cue_stick.position.z
				#, _stick_min_z, _stick_max_z)

func _handle_shot_input():
	if (Input.is_action_just_pressed("shoot") and
			_game_state.current_play_state == Enums.PlayState.AIMING):
		_stick_animation_player.play("shoot_stick")

# _stick_animation_player execute this
func _strike_ball():
	var stick_direction = -_aim_container.basis.z
	var shot_power = lerp(_shot_power_min, _shot_power_max, _shot_percent)
	var shot_vector = stick_direction * shot_power
	_cue_ball.apply_central_impulse(shot_vector)
	
	_cue_stick.visible = false
	
	_game_state.current_play_state = Enums.PlayState.BALLS_IN_PLAY
	
	GameEvents.cue_ball_hit.emit()

func _setup_next_shot():
	_cue_stick.visible = true
	_aim_cam.make_current()
	_shot_percent = 0.0
	
	if _game_state.current_play_state == Enums.PlayState.BALL_IN_HAND:
		_cue_ball.position = BilliardTable.HEAD_SPOT
		_cue_ball.linear_velocity = Vector3.ZERO
		_cue_ball.angular_velocity = Vector3.ZERO
		_cue_ball.set_freeze_state(false)
		_game_state.current_play_state = Enums.PlayState.AIMING


#func _process_cheat_mode():
#	_cue_ball.apply_central_force(Vector3(
#			Input.get_action_strength("ui_right")
#				- Input.get_action_strength("ui_left"),
#			0,
#			Input.get_action_strength("ui_down")
#				- Input.get_action_strength("ui_up")
#	) * 10)
