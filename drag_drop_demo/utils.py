

def handle_dragging(command_blocks, sequence_area, sequence):
    for block in command_blocks:
        if block.dragging and block.rect.colliderect(sequence_area):
            if len(sequence) <= 10: #cant drag any more commands after 10 are in the sequence area
                sequence.append(block.text)
                block.rect.x, block.rect.y = 50, 50+command_blocks.index(block)*60
                block.dragging =False
