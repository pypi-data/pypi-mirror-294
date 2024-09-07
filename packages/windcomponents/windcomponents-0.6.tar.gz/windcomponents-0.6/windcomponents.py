import math


class RunwayWindComponents:
    def __init__(self, rwy_direction):
        self.rwy_direction = rwy_direction
        self.cross_tail_wind_directions = self._define_cross_tail_wind_directions()
        # this gets executed when calling the class in another py file by user to extract this output as input for local calculations


    def _define_cross_tail_wind_directions(self):
    # function starts with _ since only called internally, not by user

        # INDEXING LISTS OF COMPASS DIRECTIONS
        rwy_directions_list_clockwise = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350,
            0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350]
        rwy_directions_list_anticlockwise = [0,350,340,330,320,310,300,290,280,270,260,250,240,230,220,210,200,190,180,170,160,150,140,130,120,110,100,90,80,70,60,50,40,30,20,10,0,
            350,340,330,320,310,300,290,280,270,260,250,240,230,220,210,200,190,180,170,160,150,140,130,120,110,100,90,80,70,60,50,40,30,20,10]
        # a separate list is required for anticlockwise since else if going in the reverse order in the clockwise list - to account for anti clockwise, you can end to the left (outside) of that list
        # 2x the directions series in both lists (2x same sequence, so you never end up outside when moving towards the right)

        # TAILWIND LEFT SIDE
        tailwind_central_direction = (self.rwy_direction + 180) % 360
        # inverse of RWY heading delivers the starting direction of the wind which is tailwind
        # modulo 360 to ensure you stay within 360 deg system instead of continuing with 370, 380, etc - so with module after 360 it takes the remainder = like starting from 0 again
        # print(tailwind_central_direction)

        index_of_direction = rwy_directions_list_clockwise.index(tailwind_central_direction)
        # leftside is from tail of RWY to the left so clockwise, hence take that list
        tailwind_directions_leftside = rwy_directions_list_clockwise[index_of_direction : index_of_direction + 9]
        # there are always 9 directions in each quadrant list
        # full tailwind can (and should) be in both lists (left, right tailwind lists) since in if then else structure below only 1 condition applies
        # print(f'tailwind directions left side: {tailwind_directions_leftside}')

        # TAILWIND RIGHT SIDE
        index_of_direction = rwy_directions_list_anticlockwise.index(tailwind_central_direction)
        # rightside is from tail of RWY to the right so anticlockwise, hence take that list
        tailwind_directions_rightside = rwy_directions_list_anticlockwise[index_of_direction : index_of_direction + 9]
        # there are always 9 directions in each quadrant list
        # full tailwind can (and should) be in both lists (left, right tailwind lists) since in if then else structure below only 1 condition applies
        # print(f'tailwind directions right side: {tailwind_directions_rightside}')

        # FULL TAILWIND DIRECTIONS
        tailwind_directions = (tailwind_directions_leftside + tailwind_directions_rightside)
        tailwind_directions = set(tailwind_directions)
        # left and rightside lists both contain the wind direction for full tailwind, so make it a 'set' with unique values only here

        # CROSSWIND FRONT LEFT
        index_of_direction = rwy_directions_list_anticlockwise.index(self.rwy_direction)
        # leftside front is anticlockwise (to ensure crosswind angle increases with every step), hence take that list
        start_index_crosswind_directions_front_leftside = index_of_direction + 1
        # crosswind front left starts 1 position in the list from the rwy_direction index onwards, since the RWY direction itself is headwind, no crosswind
        crosswind_directions_front_leftside = rwy_directions_list_anticlockwise[start_index_crosswind_directions_front_leftside : start_index_crosswind_directions_front_leftside + 9]
        # there are always 9 directions in each quadrant list
        # print(f'crosswind directions front left side: {crosswind_directions_front_leftside}')

        # CROSSWIND BACK LEFT
        index_of_direction = rwy_directions_list_clockwise.index(tailwind_central_direction)
        # leftside back is clockwise (to ensure crosswind angle increases with every step), hence take that list
        start_index_crosswind_directions_back_leftside = index_of_direction + 1
        # crosswind back leftside starts 1 position in list from the full tailwind direction, since tailwind <> crosswind, crosswind starts 1 position later on in the list
        # clockwise ensures that the crosswind angle increases in magnitude until reaching full crosswind 90 deg angle
        crosswind_directions_back_leftside = rwy_directions_list_clockwise[start_index_crosswind_directions_back_leftside : start_index_crosswind_directions_back_leftside + 9]
        # there are always 9 directions in each quadrant list
        # print(f'crosswind directions back left side: {crosswind_directions_back_leftside}')

        # CROSSWIND FRONT RIGHT
        index_of_direction = rwy_directions_list_clockwise.index(self.rwy_direction)
        # rightside front is clockwise (to ensure crosswind angle increases with every step), hence take that list
        start_index_crosswind_directions_front_rightside = index_of_direction + 1
        # crosswind front right starts 1 position in the list from the rwy_direction index onwards, since the RWY direction itself is headwind, no crosswind
        crosswind_directions_front_rightside = rwy_directions_list_clockwise[start_index_crosswind_directions_front_rightside : start_index_crosswind_directions_front_rightside + 9]
        # there are always 9 directions in each quadrant list
        # print(f'crosswind directions front right side: {crosswind_directions_front_rightside}')

        # CROSSWIND BACK RIGHT
        index_of_direction = rwy_directions_list_anticlockwise.index(tailwind_central_direction)
        # rightside back is anticlockwise (to ensure crosswind angle increases with every step), hence take that list
        start_index_crosswind_directions_back_rightside = index_of_direction + 1
        # crosswind back rightside starts 1 position in list from the full tailwind direction, since tailwind <> crosswind, crosswind starts 1 position later on in the list
        # anticlockwise ensures that the crosswind angle increases in magnitude until reaching full crosswind 90 deg angle
        crosswind_directions_back_rightside = rwy_directions_list_anticlockwise[start_index_crosswind_directions_back_rightside : start_index_crosswind_directions_back_rightside + 9]
        # there are always 9 directions in each quadrant list
        # print(f'crosswind directions back right side: {crosswind_directions_back_rightside}')

        return (tailwind_directions, crosswind_directions_front_leftside, crosswind_directions_back_leftside, crosswind_directions_front_rightside, crosswind_directions_back_rightside)


    def calculate_cross_tail_head_wind(self, wind_direction, wind_speed):
        (tailwind_directions,
         crosswind_directions_front_leftside,
         crosswind_directions_back_leftside,
         crosswind_directions_front_rightside,
         crosswind_directions_back_rightside) = self.cross_tail_wind_directions
        # use data inheritance from class input (self) instead of calling other function here
        # to make sure that other function does not need to be called in each and every for loop

        # DETERMINE CROSSWIND ANGLE
        if wind_direction in crosswind_directions_front_leftside:
            position_in_list = (crosswind_directions_front_leftside.index(wind_direction) + 1)
            # + 1 since list index starts at 0, and for multiplication below needs to be at least 1, also since in respective list, only crosswind values (tailwind/headwind omitted)
            crosswind_angle = position_in_list * 10
            # since lists have been composed from small to max crosswindangle (due correct selection of clock vs anticlockwise), the position in the list is 1:1 the angle when multiplied by 10
        elif wind_direction in crosswind_directions_back_leftside:
            position_in_list = (crosswind_directions_back_leftside.index(wind_direction) + 1)
            crosswind_angle = position_in_list * 10
        elif (wind_direction in crosswind_directions_front_rightside):
            position_in_list = (crosswind_directions_front_rightside.index(wind_direction) + 1)
            crosswind_angle = position_in_list * 10
        elif wind_direction in crosswind_directions_back_rightside:
            position_in_list = (crosswind_directions_back_rightside.index(wind_direction) + 1)
            crosswind_angle = position_in_list * 10
        else:
            crosswind_angle = 0
            # in case of headwind or tailwind
        # print(f'crosswind angle: {crosswind_angle}')

        # CALCULATE CROSSWIND SPEED
        crosswind_speed = wind_speed * math.sin(math.radians(crosswind_angle))
        # use sine due crosswind angle bigger, then with sine speed component also bigger
        # https://wiki.ivao.aero/en/home/training/documentation/Crosswind_and_Headwind_calculation
        # validated with https://aerotoolbox.com/crosswind/
        # print(f'crosswind speed: {crosswind_speed}')

        # CHECK TAIL- OR HEADWIND
        if wind_direction in tailwind_directions:
            tailwind_headwind = 'tailwind'
        else:
            tailwind_headwind = 'headwind'
        # print(f'from rwy perspective, wind is tail or head: {tailwind_headwind}')

        # CALCULATE TAIL/HEADWIND SPEED
        if tailwind_headwind == 'tailwind':
            tailwind_speed = wind_speed * math.cos(math.radians(crosswind_angle))
            # use cosine due crosswind angle bigger, then tail/headwind smaller, and cosine is the inverse of sine hence big crosswind angle correctly only takes small head/tailwind relation
            # https://wiki.ivao.aero/en/home/training/documentation/Crosswind_and_Headwind_calculation
            # validated with https://aerotoolbox.com/crosswind/
            headwind_speed = 0
        else:
            tailwind_speed = 0
            headwind_speed = wind_speed * math.cos(math.radians(crosswind_angle))
        # print(f'tailwind speed: {tailwind_speed}')
        # print(f'headwind speed: {headwind_speed}')

        return (crosswind_angle, crosswind_speed, tailwind_speed, headwind_speed)
