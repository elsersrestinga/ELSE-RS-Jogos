class_name Pocket
extends Area3D



func _on_body_entered(body):
	if body is Ball:
		GameEvents.ball_potted.emit(body, self)
