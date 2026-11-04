extends Node3D

@export var _ball_tscn: PackedScene

func _ready():
	self.position = BilliardTable.FOOT_SPOT
	
	_rack_balls()

const DIAMETER = Ball.BALL_DIAMETER
const RADIUS = Ball.BALL_RADIUS

func _rack_balls():
	var num_balls = range(1, 16)
	num_balls.shuffle()
	var ball_8_index = num_balls.find(8)
	var rand_num_at_index_4 = num_balls[4]
	num_balls[4] = 8
	num_balls[ball_8_index] = rand_num_at_index_4
	
	var ball_i = 0
	for i in 5:
		for j in i+1:
			var new_ball = _ball_tscn.instantiate() as Ball
			var ball_x := i * DIAMETER * 0.9
			var ball_z := (i * RADIUS) - (j * DIAMETER)
			new_ball.setup_ball(num_balls[ball_i], ball_x, ball_z)
			self.add_child(new_ball)
			ball_i+= 1
