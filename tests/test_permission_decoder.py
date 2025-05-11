from dimo.permission_decoder import PermissionDecoder


def test_dimo_client_hex_to_permissions():
    permissions_hex = "0x3ffc"
    permissions_list = PermissionDecoder.decode_permission_bits(permissions_hex)
    assert permissions_list == [1, 2, 3, 4, 5, 6]

    one_to_five_hex = "0xffc"
    assert PermissionDecoder.decode_permission_bits(one_to_five_hex) == [1, 2, 3, 4, 5]

    another_hex = "0x3fcc"
    assert PermissionDecoder.decode_permission_bits(another_hex) == [1, 3, 4, 5, 6]
