from xml.etree.ElementTree import PI
from stl import mesh
import pygame
import numpy


def project3d_to_2d( vertex, offset ):
    # Original offset is 350

    scale = 25
    vertex = vertex * scale

    x, y, z = vertex

    r = pygame.math.Vector2(
        x - y + offset,
        x + y - z + offset
    )

    return r


def is_clockwise(points):
    v = 0
    for a, b in zip( points, points[1:] + [points[0]] ):
        v += ( b[0] - a[0] ) * ( b[1] + a[1] )
    return v > 0


def surface_normal( surface ):

    surface = numpy.array( surface )
    n = numpy.array( ( 0.0,) * 3 )

    for i, a in enumerate( surface ):
        b = surface [ ( i + 1 ) % len( surface ), : ]
        n[0] += ( a[1] - b[1] ) * ( a[2] + b[2] ) 
        n[1] += ( a[2] - b[2] ) * ( a[0] + b[0] )
        n[2] += ( a[0] - b[0] ) * ( a[1] + b[1] )

    norm = numpy.linalg.norm(n)
    if norm==0: raise ValueError('zero norm')
    return n / norm


def lerp_color( factor, color_a, color_b ):
    color_a = numpy.array(color_a)
    color_b = numpy.array(color_b)
    vector = color_b - color_a
    r = color_a + vector * factor
    return r


def sort(face):
    vertex1 = ( face[0], face[1], face[2] )
    vertex2 = ( face[3], face[4], face[5] )
    vertex3 = ( face[6], face[7], face[8] )

    m = (
        ( vertex1[0] + vertex2[0] + vertex3[0] / 3 ),
        ( vertex1[1] + vertex2[1] + vertex3[1] / 3 ),
        ( vertex1[2] + vertex2[2] + vertex3[2] / 3 ),
    )

    return m[0] + m[1] + m[2]*2


def rotate( mesh, angle_x,angle_y,angle_z):

    for face in mesh:

        vertex1 = pygame.math.Vector3( (face[0], face[1], face[2]) )
        vertex2 = pygame.math.Vector3( (face[3], face[4], face[5]) )
        vertex3 = pygame.math.Vector3( (face[6], face[7], face[8]) )
        
        # Rotation for X
        vertex1 = getattr( vertex1, 'rotate_{0}_rad'.format( 'x') )( angle_x )
        vertex2 = getattr( vertex2, 'rotate_{0}_rad'.format( 'x' ) )( angle_x )
        vertex3 = getattr( vertex3, 'rotate_{0}_rad'.format( 'x' ) )( angle_x )

        # Rotation for Y
        vertex1 = getattr( vertex1, 'rotate_{0}_rad'.format( 'y' ) )( angle_y )
        vertex2 = getattr( vertex2, 'rotate_{0}_rad'.format( 'y' ) )( angle_y )
        vertex3 = getattr( vertex3, 'rotate_{0}_rad'.format( 'y' ) )( angle_y )

        # Rotation for Z
        vertex1 = getattr( vertex1, 'rotate_{0}_rad'.format( 'z' ) )( angle_z )
        vertex2 = getattr( vertex2, 'rotate_{0}_rad'.format( 'z' ) )( angle_z )
        vertex3 = getattr( vertex3, 'rotate_{0}_rad'.format( 'z' ) )( angle_z )
                
        yield(  vertex1[0], vertex1[1], vertex1[2],
                vertex2[0], vertex2[1], vertex2[2],
                vertex3[0], vertex3[1], vertex3[2], )


def rotate_eye(faces, angle_x, angle_y, angle_z, offset, colors, ray):
        
        # Center for rotation
        """ for i in range(0, len(faces.vectors)):
            for j in range(0, len(faces.vectors[i])):
                faces.vectors[i][j] = faces.vectors[i][j] - numpy.array(offset) """

        for face in sorted( rotate( faces, angle_x, angle_y, angle_z), key = sort ):

            vertex1 = ( face[0], face[1], face[2] )
            vertex2 = ( face[3], face[4], face[5] )
            vertex3 = ( face[6], face[7], face[8] )

            polygon = [ 
                project3d_to_2d( pygame.math.Vector3( vertex ), offset=offset ) 
                for vertex in [ vertex1, vertex2, vertex3 ]  
            ]

            if is_clockwise( polygon ): continue

            n = surface_normal( [ vertex1, vertex2, vertex3 ] )

            pygame.draw.polygon(
                surface = screen,
                color = lerp_color( ( n.dot( ray ) + 1 ) / 2, *colors ),
                points = polygon,
            )

        # Reposition again for the right position
        """ for i in range(0, len(faces.vectors)):
            for j in range(0, len(faces.vectors[i])):
                faces.vectors[i][j] = faces.vectors[i][j] + numpy.array(offset) """

def render( right_faces, left_faces, right_offset, left_offset,colors, ray ):
    
    """ # Setting the Position of the Right Eye
    for i in range(0, len(right_faces.vectors)):
            for j in range(0, len(right_faces.vectors[i])):
                right_faces.vectors[i][j] = right_faces.vectors[i][j] - numpy.array(right_offset)

    # Setting the Position of the Left Eye
    for i in range(0, len(left_faces.vectors)):
            for j in range(0, len(left_faces.vectors[i])):
                left_faces.vectors[i][j] = left_faces.vectors[i][j] - numpy.array(left_offset) """

    ROTATE_SPEED = 0.02
 
    _quit = False
    angle_x = angle_y = angle_z = 0
    while not _quit:

        # screen.fill((0,0,0))
        screen.fill( 0x112233 ) 

        # Left Eye Rotations
        rotate_eye(left_faces, offset=left_offset,angle_x=angle_x,angle_y= angle_y, angle_z= angle_z,colors=colors, ray=ray)

        # Right Eye Rotations
        rotate_eye(right_faces, offset=right_offset,angle_x=-angle_x,angle_y= -angle_y, angle_z= -angle_z,colors=colors, ray=ray)


        # Pygame Events (Quitting and Using Keyboard)
        for event in  pygame.event.get():

            if event.type == pygame.QUIT:
                _quit = True
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                angle_y = angle_x = angle_z = 0
            if keys[pygame.K_a]:
                angle_y += ROTATE_SPEED
            if keys[pygame.K_d]:
                angle_y -= ROTATE_SPEED      
            if keys[pygame.K_w]:
                angle_x += ROTATE_SPEED
            if keys[pygame.K_s]:
                angle_x -= ROTATE_SPEED
            if keys[pygame.K_q]:
                angle_z -= ROTATE_SPEED
            if keys[pygame.K_e]:
                angle_z += ROTATE_SPEED  

        # Updating all the Window
        clock.tick( FPS )
        pygame.display.update()



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode( ( 800, 800 ) )
    clock = pygame.time.Clock()

    FPS = 60

    BASE_OFFSET= 350

    left_eye_offset = BASE_OFFSET + 100
    right_eye_offset = BASE_OFFSET + 0

    # test change these color to modify colors on eyes.
    # (one of the color is the shadow color)
    color_a = ( 0,   0,  0 )
    color_b = ( 200, 100, 0 )

    # the shadow is based on this vector. test change it.
    ray = pygame.math.Vector3( 0, -0.4, 0 ).normalize()

    # you can download the teapot stl file at: https://en.wikipedia.org/wiki/STL_(file_format)
    # remember to rename to to teapot.stl
    right_eye = mesh.Mesh.from_file( './meshes/new_eye.stl' )
    left_eye = mesh.Mesh.from_file( './meshes/new_eye.stl' )
    # of course you can find other stl files to test but you might have to scale and 
    # offset the projection to get a good view of it. see project3d_to_2d.

    render( right_faces=right_eye, left_faces=left_eye, left_offset=left_eye_offset, right_offset=right_eye_offset ,colors = ( color_a, color_b ), ray = ray )

    # NOTE: you can also write your own projection.
    #       implement it in project3d_to_2d (you might have to modify sort method after that)

    pygame.quit()