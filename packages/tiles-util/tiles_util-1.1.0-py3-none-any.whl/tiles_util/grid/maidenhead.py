class HamGridSquare:
    U = 'ABCDEFGHIJKLMNOPQRSTUVWX'
    L = U.lower()

    @staticmethod
    def to_num(x):
        if isinstance(x, (int, float)):
            return x
        if isinstance(x, str):
            return float(x)
        raise ValueError(f"HamGridSquare -- to_num -- cannot convert input: {x}")

    @staticmethod
    def lat_lon_to_grid_square(param1, param2=None):
        lat, lon = -100.0, 0.0

        if isinstance(param1, (list, tuple)) and len(param1) == 2:
            lat = HamGridSquare.to_num(param1[0])
            lon = HamGridSquare.to_num(param1[1])
        elif isinstance(param1, dict):
            if 'lat' in param1 and 'lon' in param1:
                lat = HamGridSquare.to_num(param1['lat']() if callable(param1['lat']) else param1['lat'])
                lon = HamGridSquare.to_num(param1['lon']() if callable(param1['lon']) else param1['lon'])
            elif 'latitude' in param1 and 'longitude' in param1:
                lat = HamGridSquare.to_num(param1['latitude']() if callable(param1['latitude']) else param1['latitude'])
                lon = HamGridSquare.to_num(param1['longitude']() if callable(param1['longitude']) else param1['longitude'])
            else:
                raise ValueError(f"HamGridSquare -- cannot convert object -- {param1}")
        else:
            lat = HamGridSquare.to_num(param1)
            lon = HamGridSquare.to_num(param2)

        if lat is None or lon is None or not isinstance(lat, float) or not isinstance(lon, float):
            raise ValueError("lat/lon must be numeric")
        if abs(lat) == 90.0:
            raise ValueError("grid squares invalid at N/S poles")
        if abs(lat) > 90:
            raise ValueError(f"invalid latitude: {lat}")
        if abs(lon) > 180:
            raise ValueError(f"invalid longitude: {lon}")

        adj_lat = lat + 90
        adj_lon = lon + 180
        g_lat = HamGridSquare.U[int(adj_lat // 10)]
        g_lon = HamGridSquare.U[int(adj_lon // 20)]
        n_lat = str(int(adj_lat % 10))
        n_lon = str(int((adj_lon // 2) % 10))
        r_lat = (adj_lat - int(adj_lat)) * 60
        r_lon = (adj_lon - 2 * int(adj_lon // 2)) * 60
        glat = HamGridSquare.L[int(r_lat // 2.5)]
        glon = HamGridSquare.L[int(r_lon // 5)]

        return g_lon + g_lat + n_lon + n_lat + glon + glat

    @staticmethod
    def grid_square_to_lat_lon(grid, obj=None):
        def lat4(g):
            return 10 * (ord(g[1]) - ord('A')) + int(g[3]) - 90

        def lon4(g):
            return 20 * (ord(g[0]) - ord('A')) + 2 * int(g[2]) - 180

        if len(grid) not in (4, 6):
            raise ValueError(f"gridSquareToLatLon: grid must be 4 or 6 chars: {grid}")

        if len(grid) == 4:
            lat = lat4(grid) + 0.5
            lon = lon4(grid) + 1.0
        elif len(grid) == 6:
            lat = lat4(grid) + (1.0 / 60.0) * 2.5 * (ord(grid[5]) - ord('a') + 0.5)
            lon = lon4(grid) + (1.0 / 60.0) * 5 * (ord(grid[4]) - ord('a') + 0.5)
        else:
            raise ValueError(f"gridSquareToLatLon: invalid grid: {grid}")

        if obj is not None:
            obj['lat'] = lat
            obj['lon'] = lon
            return obj
        return [lat, lon]

    @staticmethod
    def test_grid_square():
        print (HamGridSquare.lat_lon_to_grid_square([48.14666, 11.60833]))
        print(HamGridSquare.grid_square_to_lat_lon('JN58td'))
        # test_data = [
        #     ['Munich', [48.14666, 11.60833], 'JN58td'],
        #     ['Montevideo', [-34.91, -56.21166], 'GF15vc'],
        #     ['Washington, DC', {'lat': 38.92, 'lon': -77.065}, 'FM18lw'],
        #     ['Wellington', {'latitude': -41.28333, 'longitude': 174.745}, 'RE78ir'],
        #     ['Newington, CT (W1AW)', [41.714775, -72.727260], 'FN31pr'],
        #     ['Palo Alto (K6WRU)', [37.413708, -122.1073236], 'CM87wj'],
        #     ['Chattanooga (KI6CQ/4)', {'lat': lambda: "35.0542", 'lon': lambda: "-85.1142"}, 'EM75kb']
        # ]

        # total_passed = 0
        # for i, data in enumerate(test_data):
        #     result = HamGridSquare.lat_lon_to_grid_square(*data[1]) if isinstance(data[1], (list, tuple)) else HamGridSquare.lat_lon_to_grid_square(data[1])
        #     result2 = HamGridSquare.grid_square_to_lat_lon(result)
        #     result3 = HamGridSquare.lat_lon_to_grid_square(result2[0], result2[1])
        #     this_passed = (result == data[2]) and (result3 == data[2])
        #     print(f"test {i}: {data[0]} {data[1]} result = {result} result2 = {result2} result3 = {result3} expected = {data[2]} passed = {this_passed}")
        #     total_passed += this_passed

        # print(f"{total_passed} of {len(test_data)} tests passed")
        # return total_passed == len(test_data)

# Example usage:
HamGridSquare.test_grid_square()
