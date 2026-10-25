class_name Ball
extends RigidBody3D

const BALL_RADIUS := 0.027
const BALL_DIAMETER := BALL_RADIUS * 2

@export var _texture: Texture2D

static var num_balls_moving: int = 0

var _ball_num := 0
var ball_type : Enums.BallType = Enums.BallType.CUE_BALL

func _ready():
	GameEvents.ball_potted.connect(_on_ball_potted)
	if not self.sleeping:
		Ball.num_balls_moving += 1
	_apply_new_material()
	#$BallMesh.get_active_material(0).albedo_texture = _texture

func _physics_process(_delta):
	self.linear_velocity.y = min(BALL_DIAMETER, self.linear_velocity.y)

func setup_ball(ball_num: int, ball_x: float, ball_z: float):
	_ball_num = ball_num
	
	if ball_num == 8:
		self.ball_type = Enums.BallType.EIGHT_BALL
	elif ball_num == 0:
		self.ball_type = Enums.BallType.CUE_BALL 
	elif ball_num < 8:
		self.ball_type = Enums.BallType.LISAS
	else:
		self.ball_type = Enums.BallType.LISTRADAS
		
	
	self.position.x = ball_x
	self.position.z = ball_z
	
	_texture = load("res://assets/textures/" + str(ball_num) + ".jpg")
	_apply_new_material() 

func is_object_ball() -> bool:
	return (self.ball_type == Enums.BallType.LISAS
			or self.ball_type == Enums.BallType.LISTRADAS)


func set_freeze_state(new_freeze_state: bool):
	self.freeze = new_freeze_state
	self.sleeping = new_freeze_state
	self.sleeping_state_changed.emit()


func _apply_new_material():
	var new_material = StandardMaterial3D.new()
	new_material.albedo_texture = _texture
	$BallMesh.material_override = new_material


func _on_sleeping_state_changed():
	if self.sleeping:
		Ball.num_balls_moving -= 1
	else:
		Ball.num_balls_moving += 1
	if Ball.num_balls_moving == 0:
		GameEvents.all_balls_stopped.emit()
	#print("current balls moving: ", Ball.num_balls_moving)

func _on_ball_potted(ball, _pocket):
	if (ball == self):
		self.set_freeze_state(true)
		self.position = Vector3(0, -0.5, 0)
		
