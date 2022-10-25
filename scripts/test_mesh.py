from xml.etree.ElementTree import PI
from stl import mesh
import pygame
import numpy
import math


def project3d_to_2d( vertex ):

    scale = 25
    vertex = vertex * scale

    x, y, z = vertex

    r = pygame.math.Vector2(
        x - y + 350,
        x + y - z + 350
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


def rotate( mesh, angle_x,angle_y,angle_z, rot_x, rot_y, rot_z ):

    for face in mesh:

        # Rotation for X
        vertex1 = pygame.math.Vector3( (face[0], face[1], face[2]) )
        vertex2 = pygame.math.Vector3( (face[3], face[4], face[5]) )
        vertex3 = pygame.math.Vector3( (face[6], face[7], face[8]) )
        
        vertex1 = getattr( vertex1, 'rotate_{0}_rad'.format( rot_x ) )( angle_x )
        vertex2 = getattr( vertex2, 'rotate_{0}_rad'.format( rot_x ) )( angle_x )
        vertex3 = getattr( vertex3, 'rotate_{0}_rad'.format( rot_x ) )( angle_x )

        """  yield(  vertex1[0], vertex1[1], vertex1[2],
                vertex2[0], vertex2[1], vertex2[2],
                vertex3[0], vertex3[1], vertex3[2], ) """

        # Rotation for Y
        vertex4 = pygame.math.Vector3( (face[0], face[1], face[2]) )
        vertex5 = pygame.math.Vector3( (face[3], face[4], face[5]) )
        vertex6 = pygame.math.Vector3( (face[6], face[7], face[8]) )

        vertex1 = getattr( vertex1, 'rotate_{0}_rad'.format( rot_y ) )( angle_y )
        vertex2 = getattr( vertex2, 'rotate_{0}_rad'.format( rot_y ) )( angle_y )
        vertex3 = getattr( vertex3, 'rotate_{0}_rad'.format( rot_y ) )( angle_y )

        """ yield(  vertex4[0], vertex4[1], vertex4[2],
                vertex5[0], vertex5[1], vertex5[2],
                vertex6[0], vertex6[1], vertex6[2], ) """

        # Rotation for Z
        vertex7 = pygame.math.Vector3( (face[0], face[1], face[2]) )
        vertex8 = pygame.math.Vector3( (face[3], face[4], face[5]) )
        vertex9 = pygame.math.Vector3( (face[6], face[7], face[8]) )

        vertex1 = getattr( vertex1, 'rotate_{0}_rad'.format( rot_z ) )( angle_z )
        vertex2 = getattr( vertex2, 'rotate_{0}_rad'.format( rot_z ) )( angle_z )
        vertex3 = getattr( vertex3, 'rotate_{0}_rad'.format( rot_z ) )( angle_z )

        """ yield ( vertex7[0], vertex7[1], vertex7[2],
                vertex8[0], vertex8[1], vertex8[2],
                vertex9[0], vertex9[1], vertex9[2], ) """
                
        yield(  vertex1[0], vertex1[1], vertex1[2],
                vertex2[0], vertex2[1], vertex2[2],
                vertex3[0], vertex3[1], vertex3[2], )


def render( faces, x_rot, y_rot, z_rot, colors, ray ):
    
    screen.fill( 0x112233 ) 

    for face in sorted( rotate( faces, x_rot, y_rot, z_rot, 'x', 'y', 'z' ), key = sort ):

        vertex1 = ( face[0], face[1], face[2] )
        vertex2 = ( face[3], face[4], face[5] )
        vertex3 = ( face[6], face[7], face[8] )

        polygon = [ 
            project3d_to_2d( pygame.math.Vector3( vertex ) ) 
            for vertex in [ vertex1, vertex2, vertex3 ]  
        ]

        if is_clockwise( polygon ): continue

        n = surface_normal( [ vertex1, vertex2, vertex3 ] )

        pygame.draw.polygon(
            surface = screen,
            color = lerp_color( ( n.dot( ray ) + 1 ) / 2, *colors ),
            points = polygon,
        )

    ROTATE_SPEED = 0.02
 
    _quit = False
    angle_x = angle_y = angle_z = 0
    while not _quit:

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


        clock.tick( FPS )
        pygame.display.update()



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode( ( 700, 700 ) )
    clock = pygame.time.Clock()

    FPS = 60

    # test change this value to rotate the teapot ( it is in radians )
    # z_positive = counter_clockwise
    
    x_rot = (math.pi) / 2
    y_rot = (math.pi) / 2
    z_rot = 0

    # test change these color to modify colors on teapot.
    # (one of the color is the shadow color)
    color_a = ( 0,   0,  0 )
    color_b = ( 200, 100, 0 )

    # the shadow is based on this vector. test change it.
    ray = pygame.math.Vector3( 0, -0.4, 0 ).normalize()

    # you can download the teapot stl file at: https://en.wikipedia.org/wiki/STL_(file_format)
    # remember to rename to to teapot.stl
    faces = mesh.Mesh.from_file( './meshes/teapot.stl' )
    # of course you can find other stl files to test but you might have to scale and 
    # offset the projection to get a good view of it. see project3d_to_2d.

    render( faces, x_rot = x_rot, y_rot = y_rot , z_rot = z_rot, colors = ( color_a, color_b ), ray = ray )

    # NOTE: you can also write your own projection.
    #       implement it in project3d_to_2d (you might have to modify sort method after that)

    pygame.quit()