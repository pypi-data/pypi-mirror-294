import pytest
from datetime import datetime
from pydantic.v1.error_wrappers import ValidationError

from ogmios.datatypes import (
    Origin,
    Point,
    Tip,
    Block,
    GenesisConfiguration,
    ProtocolParameters,
    BootstrapProtocolParameters,
)
from ogmios.model.model_map import Types
import ogmios.model.ogmios_model as om

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_Origin():
    # Valid origin
    origin = Origin()
    assert origin._schematype == om.Origin.origin


def test_Point():
    # Valid Point
    Point(slot=10, id="45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af")

    # Invalid slot
    with pytest.raises(ValidationError):
        Point(slot=-10, id="45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af")

    # Invalid id
    with pytest.raises(ValidationError):
        Point(slot=10, id="bad_id")


def test_Tip():
    # Valid Tip
    Tip(slot=10, height=1000, id="45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af")

    # Invalid slot
    with pytest.raises(ValidationError):
        Tip(
            slot=-10,
            height=1000,
            id="45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
        )

    # Invalid height
    with pytest.raises(ValidationError):
        Tip(
            slot=10,
            height=-1000,
            id="45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
        )

    # Invalid id
    with pytest.raises(ValidationError):
        Tip(slot=10, height=1000, id="bad_id")


def test_Tip_to_point():
    tip = Tip(
        slot=10, height=1000, id="45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af"
    )
    point = Point(slot=10, id="45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af")
    assert tip.to_point() == point


def test_Block_EBB():
    # Valid EBB block
    kwargs = {
        "era": "byron",
        "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
        "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
        "height": 100,
    }
    Block(Types.ebb.value, **kwargs)

    # Wrong era
    with pytest.raises(ValidationError):
        kwargs = {
            "era": "shelley",
            "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "height": 100,
        }
        Block(Types.ebb.value, **kwargs)

    # Invalid height
    with pytest.raises(ValidationError):
        kwargs = {
            "era": "byron",
            "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "height": -100,
        }
        Block(Types.ebb.value, **kwargs)

    # Missing required parameter
    with pytest.raises(ValidationError):
        kwargs = {
            "era": "byron",
            "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "height": 100,
        }
        Block(Types.ebb.value, **kwargs)


def test_Block_BFT():
    # Valid block
    kwargs = {
        "era": "byron",
        "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
        "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
        "height": 100,
        "slot": 1000,
        "size": {"bytes": 1},
        "transactions": [],  # TODO: Add this type
        "protocol": {
            "id": 123456,
            "version": {"major": 0, "minor": 1, "patch": 2},
            "software": {"appName": "test", "number": 1234},
        },
        "issuer": {
            "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af"
        },
        "delegate": {
            "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af"
        },
    }
    Block(Types.bft.value, **kwargs)

    # Wrong era
    with pytest.raises(ValidationError):
        kwargs = {
            "era": "shelley",
            "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "height": 100,
            "slot": 1000,
            "size": {"bytes": 1},
            "transactions": [],  # TODO: Add this type
            "protocol": {
                "id": 123456,
                "version": {"major": 0, "minor": 1, "patch": 2},
                "software": {"appName": "test", "number": 1234},
            },
            "issuer": {
                "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af"
            },
            "delegate": {
                "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af"
            },
        }
        Block(Types.bft.value, **kwargs)

    # Invalid height
    with pytest.raises(ValidationError):
        kwargs = {
            "era": "byron",
            "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "height": -100,
            "slot": 1000,
            "size": {"bytes": 1},
            "transactions": [],  # TODO: Add this type
            "protocol": {
                "id": 123456,
                "version": {"major": 0, "minor": 1, "patch": 2},
                "software": {"appName": "test", "number": 1234},
            },
            "issuer": {
                "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af"
            },
            "delegate": {
                "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af"
            },
        }
        Block(Types.bft.value, **kwargs)

    # Missing required parameter
    with pytest.raises(ValidationError):
        kwargs = {
            "era": "byron",
            "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "slot": 1000,
            "size": {"bytes": 1},
            "transactions": [],  # TODO: Add this type
            "protocol": {
                "id": 123456,
                "version": {"major": 0, "minor": 1, "patch": 2},
                "software": {"appName": "test", "number": 1234},
            },
            "issuer": {
                "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af"
            },
            "delegate": {
                "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af"
            },
        }
        Block(Types.bft.value, **kwargs)


def test_Block_Praos():
    # Valid block
    kwargs = {
        "era": "alonzo",
        "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
        "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
        "nonce": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
        "height": 100,
        "slot": 1000,
        "size": {"bytes": 1},
        "transactions": [],  # TODO: Add this type
        "protocol": {
            "version": {"major": 0, "minor": 1, "patch": 2},
        },
        "issuer": {
            "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "vrfVerificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "operationalCertificate": {
                "count": 123,
                "kes": {
                    "period": 12,
                    "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
                },
            },
            "leaderValue": {},
        },
    }
    Block(Types.praos.value, **kwargs)

    # Wrong era
    with pytest.raises(ValidationError):
        kwargs = {
            "era": "byron",
            "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "nonce": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "height": 100,
            "slot": 1000,
            "size": {"bytes": 1},
            "transactions": [],  # TODO: Add this type
            "protocol": {
                "version": {"major": 0, "minor": 1, "patch": 2},
            },
            "issuer": {
                "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
                "vrfVerificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
                "operationalCertificate": {
                    "count": 123,
                    "kes": {
                        "period": 12,
                        "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
                    },
                },
                "leaderValue": {},
            },
        }
        Block(Types.praos.value, **kwargs)

    # Invalid height
    with pytest.raises(ValidationError):
        kwargs = {
            "era": "babbage",
            "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "nonce": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "height": -100,
            "slot": 1000,
            "size": {"bytes": 1},
            "transactions": [],  # TODO: Add this type
            "protocol": {
                "version": {"major": 0, "minor": 1, "patch": 2},
            },
            "issuer": {
                "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
                "vrfVerificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
                "operationalCertificate": {
                    "count": 123,
                    "kes": {
                        "period": 12,
                        "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
                    },
                },
                "leaderValue": {},
            },
        }
        Block(Types.praos.value, **kwargs)

    # Missing required parameter
    with pytest.raises(ValidationError):
        kwargs = {
            "era": "shelley",
            "id": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "ancestor": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
            "slot": 1000,
            "size": {"bytes": 1},
            "transactions": [],  # TODO: Add this type
            "protocol": {
                "version": {"major": 0, "minor": 1, "patch": 2},
            },
            "issuer": {
                "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
                "vrfVerificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
                "operationalCertificate": {
                    "count": 123,
                    "kes": {
                        "period": 12,
                        "verificationKey": "45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af",
                    },
                },
                "leaderValue": {},
            },
        }
        Block(Types.praos.value, **kwargs)


def test_GenesisConfiguration_byron():
    valid_config = {
        "era": "byron",
        "genesis_key_hashes": ["90181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d3"],
        "genesis_delegations": {
            "property1": {
                "issuer": {
                    "verificationKey": "stringstringstringstringstringstringstringstringstringstringstri"
                },
                "delegate": {
                    "verificationKey": "stringstringstringstringstringstringstringstringstringstringstri"
                },
            },
            "property2": {
                "issuer": {
                    "verificationKey": "stringstringstringstringstringstringstringstringstringstringstri"
                },
                "delegate": {
                    "verificationKey": "stringstringstringstringstringstringstringstringstringstringstri"
                },
            },
        },
        "start_time": "2019-08-24T14:15:22Z",
        "initial_funds": {
            "property1": {"ada": {"lovelace": 0}},
            "property2": {"ada": {"lovelace": 0}},
        },
        "initial_vouchers": {
            "property1": {"ada": {"lovelace": 0}},
            "property2": {"ada": {"lovelace": 0}},
        },
        "security_parameter": 18446744073709552000,
        "network_magic": 764824073,
        "updatable_parameters": {
            "scriptVersion": 0,
            "slotDuration": 20000,
            "maxBlockBodySize": {"bytes": 2000000},
            "maxBlockHeaderSize": {"bytes": 2000000},
            "maxTransactionSize": {"bytes": 4096},
            "maxUpdateProposalSize": {"bytes": 700},
            "multiPartyComputationThreshold": "1/50",
            "heavyDelegationThreshold": "3/10000",
            "updateVoteThreshold": "1/1000",
            "updateProposalThreshold": "1/10",
            "updateProposalTimeToLive": 10000,
            "unlockStakeEpoch": 18446744073709551615,
            "softForkInitThreshold": "9/10",
            "softForkMinThreshold": "3/5",
            "softForkDecrementThreshold": "1/20",
            "minFeeConstant": {"ada": {"lovelace": 155381}},
            "minFeeCoefficient": 44,
        },
    }

    genesis_configuration = GenesisConfiguration(**valid_config)
    assert genesis_configuration.era == "byron"
    assert genesis_configuration.genesis_key_hashes == [
        "90181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d3"
    ]
    assert genesis_configuration.genesis_delegations.keys() == {"property1", "property2"}
    assert isinstance(genesis_configuration.start_time, datetime)
    assert genesis_configuration.initial_funds.keys() == {"property1", "property2"}
    assert genesis_configuration.initial_vouchers.keys() == {"property1", "property2"}
    assert genesis_configuration.security_parameter == 18446744073709552000
    assert genesis_configuration.network_magic == 764824073
    assert isinstance(genesis_configuration.updatable_parameters, BootstrapProtocolParameters)

    # Optional ProtocolParameters
    valid_config.pop("updatable_parameters")
    genesis_configuration = GenesisConfiguration(**valid_config)
    assert isinstance(genesis_configuration, GenesisConfiguration)

    # Missing required parameter
    invalid_config = valid_config.copy()
    invalid_config.pop("era")
    with pytest.raises(TypeError):
        GenesisConfiguration(**invalid_config)


def test_GenesisConfiguration_shelley():
    valid_config = {
        "era": "shelley",
        "start_time": "1864-05-14T12:52:58Z",
        "network_magic": 5,
        "network": "mainnet",
        "active_slots_coefficient": "1338933938837/2500000000000",
        "security_parameter": 6,
        "epoch_length": 10,
        "slots_per_kes_period": 8,
        "max_kes_evolutions": 12,
        "slot_length": {"milliseconds": 5500000000},
        "update_quorum": 3,
        "max_lovelace_supply": 6,
        "initial_parameters": {
            "minFeeCoefficient": 334307,
            "minFeeConstant": {"ada": {"lovelace": 32519}},
            "maxBlockBodySize": {"bytes": 2},
            "maxBlockHeaderSize": {"bytes": 4},
            "maxTransactionSize": {"bytes": 0},
            "stakeCredentialDeposit": {"ada": {"lovelace": 59105}},
            "stakePoolDeposit": {"ada": {"lovelace": 656520}},
            "stakePoolRetirementEpochBound": 9,
            "desiredNumberOfStakePools": 2,
            "stakePoolPledgeInfluence": "6944763091873046659/10000000000000000",
            "minStakePoolCost": {"ada": {"lovelace": 799263}},
            "monetaryExpansion": "2337923867682421/2500000000000000",
            "treasuryExpansion": "494551394454573889/1000000000000000000",
            "federatedBlockProductionRatio": "1/10",
            "extraEntropy": "7cf8ec2696b93e93d87cb1d59cbe9343aefc774d68313a1d8a9fc38c5d86009d",
            "minUtxoDepositConstant": {"ada": {"lovelace": 459786}},
            "minUtxoDepositCoefficient": 0,
            "version": {"major": 9, "minor": 5},
        },
        "initial_delegates": [
            {
                "issuer": {"id": "071ca6ccedf196ddca60d8522e04f670a715a5a0da17745ed7af8028"},
                "delegate": {
                    "id": "888e976949b0b94df754d2776bc0e95347d702c36bef13dabb7cb344",
                    "vrfVerificationKeyHash": "e66a75f9333b7ac5039b213b03c10e72b50f240236f04ae1660afa8e2dbf3ee6",
                },
            },
            {
                "issuer": {"id": "50d964d38f17b9a90884fb467798b6af0aab2b3a26f6a4b64e97c06e"},
                "delegate": {
                    "id": "2f424be0813e119d4b8b17138249ca9472ae7d7e3691a23a9219a18f",
                    "vrfVerificationKeyHash": "02bc1caadd2c65e15d20e942bd60d18035536f2a6c69aaaa8f15292a70e183b4",
                },
            },
            {
                "issuer": {"id": "a75b569648ca237f9f8627938492b19540a9b3501a1f8de3d95b42df"},
                "delegate": {
                    "id": "9d094b662fd67b342363cdc5f325717a002c4e9f2981b23e4a3f1bed",
                    "vrfVerificationKeyHash": "5245b1fd132c574ace1b7745386b7862b4bb9c7a9dddeb99f825e54d3d8840de",
                },
            },
        ],
        "initial_funds": {
            "addr1z9wpmfm7tvvw8rzclyj4r03vfemjcm2gnnphxny2524qz22gtfcw7qeul7s0rhuyatk2dmhjh43f20y8x2rt68mymqcshvjs4y": {
                "ada": {"lovelace": 841057}
            },
            "addr_test1zzuht8ecma93glf73engw92g7ckyve2tex49rvl5lzm0uzggx4mxyh5ud6yq5pzfcg5pl7gs6msyq6a87j0lkwuhs67qxlwfkc": {
                "ada": {"lovelace": 834989}
            },
            "addr1v8nwyquhku0anazevzmvczuh7x5kwzaqxaq60gz2mkq0zkg34ce0f": {
                "ada": {"lovelace": 535223}
            },
            "addr_test1qr4rjx0aeah96mfx3el5ay3a4cp87ckh9xpr5wcmhd2q08xprvnuhndwmzq70gw25azaxwya8j7mltthcr9xglk3kgcssydgnf": {
                "ada": {"lovelace": 750137}
            },
            "addr_test1wrh49wsfwua290nx025w36yqn5mrrgxpzlxp39per6rl58s0suyje": {
                "ada": {"lovelace": 35407}
            },
        },
        "initial_stake_pools": {
            "stakePools": {
                "pool1426r0jwht0kv596l4r7pvhaqcj4c7afu8u0tc8r5mawdj5wkcwm": {
                    "id": "pool1426r0jwht0kv596l4r7pvhaqcj4c7afu8u0tc8r5mawdj5wkcwm",
                    "vrfVerificationKeyHash": "32289a42d0f9a33f0a1a0a0db7e310e07eb9073c1a3386af633a18ac164ed4de",
                    "pledge": {"ada": {"lovelace": 164537}},
                    "cost": {"ada": {"lovelace": 565775}},
                    "margin": "184631597529/200000000000",
                    "rewardAccount": "stake_test17z4f3g8kzeywj4wece4xtszj3wgnl73d4cx63u0svm0v38clcpjyn",
                    "owners": [
                        "24c5583cba1ebdc321de0a088812de63d8f63dae6aa377706e0d7fc5",
                        "71ccf716b9fd239cbff71c336fac46c04947d542bd216a8c3fd26412",
                        "a7022530cb18c3723fabbe8e9c42bc82d36c33e3355eeb993bb89469",
                    ],
                    "relays": [
                        {
                            "type": "hostname",
                            "hostname": "RwbiBR7jFIukrTsv7PrUW05gJydEfSlC3.com",
                        },
                        {"type": "ipAddress", "ipv4": "0.0.0.6", "ipv6": "0:8:0:1::3"},
                    ],
                    "metadata": {
                        "url": "https://PBAzsHajgW0rK1JV5eTCLCpecLrLxi8AG-z4.com",
                        "hash": "36",
                    },
                },
                "pool1f224p497547tz5xdy77rxmz5dc5ntr93xqm3dym8s9xqc9htk20": {
                    "id": "pool1f224p497547tz5xdy77rxmz5dc5ntr93xqm3dym8s9xqc9htk20",
                    "vrfVerificationKeyHash": "a382f459aa026bc31762cdf3019e260a6c1e849dc0fcc17475a8f9bbe21b99ce",
                    "pledge": {"ada": {"lovelace": 334945}},
                    "cost": {"ada": {"lovelace": 56740}},
                    "margin": "65983/200000",
                    "rewardAccount": "stake_test17p6wetcm4treyrczfl34qknmhuc4fke82qj2evmckvfne9qqem4cc",
                    "owners": [
                        "2769036cf196b9a5c81acf0203d86bdfc6197d93fbd29fc8998e2920",
                        "2aa79a3d455ca1d25b832d32b3e77c4f3cec0ffb3c86076ec2f4e040",
                        "3e17b471d1c0d937bc6ffded4a89f72cd5da7771de12fcbf8d44d3db",
                        "aa6d101aacf21268f05c781be0883fd0d4455613547d3b0c00701d37",
                    ],
                    "relays": [
                        {"type": "hostname", "hostname": "73aNjh.com", "port": 5},
                        {"type": "ipAddress", "ipv4": "0.0.0.5"},
                        {
                            "type": "hostname",
                            "hostname": "LcgxHyKpFChdVoH74KKsYCrZwIh3N57.com",
                            "port": 6,
                        },
                        {
                            "type": "hostname",
                            "hostname": "JbKSORwhO2oQAuE5mN8V40tgOOj15wXheruygSDgvIoxmhJrG.com",
                            "port": 7,
                        },
                        {"type": "hostname", "hostname": "hgDgYDlteF1fDzxWwQuIZeB6xWE.com"},
                    ],
                    "metadata": {"url": "https://hw1dJ.com", "hash": "67"},
                },
                "pool1s4cad3jtkyml5e9qwv7qf8jhedhc5wrck6qwak040dtaw0rysyn": {
                    "id": "pool1s4cad3jtkyml5e9qwv7qf8jhedhc5wrck6qwak040dtaw0rysyn",
                    "vrfVerificationKeyHash": "09e7a2aff4f9d88bff2d8282901138cc11ff63c7c35956916236e369c04ca53c",
                    "pledge": {"ada": {"lovelace": 228853}},
                    "cost": {"ada": {"lovelace": 3368}},
                    "margin": "53/100",
                    "rewardAccount": "stake17xa2ac634h9dvg2l0f8qcagmk5j0ktfh06hvslv4wxlsumg5nr854",
                    "owners": [
                        "2c77808a0001a0fcdb3ed6ce92244c54840fa4f7c9de47371838ddfa",
                        "4af4dfc5a82720536fc190d4d128db954bcddbab7f30d7167d916d02",
                        "938f183de817cf3fe4fd2c3f1937b738aa4c9c5b9b5206d65fafd85d",
                    ],
                    "relays": [
                        {"type": "hostname", "hostname": "y0pcPeUIh.com", "port": 5},
                        {
                            "type": "hostname",
                            "hostname": "SxqqQlUfHfN0jc6BXgO-T3Z9k.com",
                            "port": 1,
                        },
                        {"type": "ipAddress", "ipv6": "0:1:0:6:0:8:0:8", "port": 4},
                    ],
                    "metadata": {"url": "https://3LF4CEoIywCrowxJg.com", "hash": "8ef7"},
                },
                "pool19r2pczfq2dsphsgdkpaf8a297ejhvve654l4e37dmawmslkyncp": {
                    "id": "pool19r2pczfq2dsphsgdkpaf8a297ejhvve654l4e37dmawmslkyncp",
                    "vrfVerificationKeyHash": "ad83c09143c7557bdf2347fc1347909ee18baa7a8af74c3564777c2c3b6156f4",
                    "pledge": {"ada": {"lovelace": 440636}},
                    "cost": {"ada": {"lovelace": 778485}},
                    "margin": "1/1",
                    "rewardAccount": "stake_test17q99v6j2rd94cs4ttpc9yrm94rllc3ncu25tkxxrdw2upgq06qauy",
                    "owners": [
                        "0abf0d596e8c41c982bd786d678e3b682ecc19ec99ee9a6db32ae4ad",
                        "33e56066c25ee952b1819e4a4e1479c4b76dfe5a7832c0f3d93e05fb",
                        "b47d4d14662f8bdb2a3e24bdb050dccb29281c8e955ff89427ad0f0f",
                    ],
                    "relays": [
                        {
                            "type": "hostname",
                            "hostname": "VxRy-dXxjkx5h3v3b6rs4tKwdVIzkADgLnqx4a90R.com",
                            "port": 8,
                        },
                        {
                            "type": "hostname",
                            "hostname": "dLS1PsH5ugzRm50zC0Nh8lcW7D1MFUXQwptSoNl5.com",
                        },
                    ],
                    "metadata": {"url": "https://10t.q.r9H2.com", "hash": "ead416569a"},
                },
                "pool1kqmu4u6zdjfnq7kexlutyzatsnsappe0z4hlzynynam7ut93e9u": {
                    "id": "pool1kqmu4u6zdjfnq7kexlutyzatsnsappe0z4hlzynynam7ut93e9u",
                    "vrfVerificationKeyHash": "5caa1ab0c9fc65d8bb55abad44d1c9abc7e544ec46934c5714364899741a7f66",
                    "pledge": {"ada": {"lovelace": 840868}},
                    "cost": {"ada": {"lovelace": 861373}},
                    "margin": "899/1000",
                    "rewardAccount": "stake178mq5uq0pdwsqxgxqrkkehffupun584warusx4p3kk9t7scn7a9zm",
                    "owners": [
                        "83203768841eefd9a04408180cfc2ff4a0cd4103bf161f71062e4395",
                        "bbb49b1cd27e36f051a35bb1de62d2bd5987e99123abf96a6e386247",
                        "d5029d809f698e41168e378a4304be24a5dca539b40d8a46d3d391dd",
                    ],
                    "relays": [
                        {"type": "hostname", "hostname": "GDLiIPxGMSudxNn.com", "port": 2},
                        {
                            "type": "hostname",
                            "hostname": "rw.yqNDbCKLNuD5KOU165XZgbbu.com",
                            "port": 5,
                        },
                        {"type": "ipAddress", "ipv6": "0:0:0:2::"},
                        {"type": "hostname", "hostname": "BpggE8Aq8hQRoelEM1Mc5eB.com"},
                        {
                            "type": "hostname",
                            "hostname": "ltBJLzo0oFxAbUsfsBbU9mK31e2JBdK.XGNL.40I2JJ8Zxu9RB8.com",
                        },
                        {
                            "type": "ipAddress",
                            "ipv4": "0.0.0.1",
                            "ipv6": "0:4:0:7:0:4:0:1",
                            "port": 7,
                        },
                    ],
                    "metadata": {
                        "url": "https://gSkhfClLO4qMnlKUh9Ykk26.p4OI84uvRZ12TVqCWX4.com",
                        "hash": "7326",
                    },
                },
                "pool1evy8aa4dpmchen4yspjsc9x6j38jtxjqz556getkj860jnpqa4w": {
                    "id": "pool1evy8aa4dpmchen4yspjsc9x6j38jtxjqz556getkj860jnpqa4w",
                    "vrfVerificationKeyHash": "f9f3f88ee69184d618951f8226b4ca6c8df7ece09a53f5233af95df731891735",
                    "pledge": {"ada": {"lovelace": 729846}},
                    "cost": {"ada": {"lovelace": 559218}},
                    "margin": "1706179828357/2500000000000",
                    "rewardAccount": "stake_test1urqm8w75x8pkgw0kwytxullk9ccrk20n9ytwdvl33afdkwc5t59j4",
                    "owners": [
                        "097303a5ae59a8c95923a021d6ea259f16e70769fc06ad98208750dd",
                        "c405c0a0d6113294d82f539c8ad6ec603e92bd6e2c1b138f4b0866d6",
                    ],
                    "relays": [],
                    "metadata": {
                        "url": "https://uXdMiE3GKmjrbNMkFNQPNzOZjGUZ9WYU.com",
                        "hash": "f5eb",
                    },
                },
            },
            "delegators": {
                "cc4cae00c233b43d6c8319ebdfdcab69e408f9cc2c4f1cf45a889860": "pool1pxn5uhu8kz5qecpgdzfxs68fh58z7q0ld56qsn3us94asvtrw2x",
                "a9929526d7eeb5d47d5853ffa17dfd013c2387c31c3e3d8732856c2f": "pool1322heh7ry3u5h53ahzx443t8n6tymv5h933twrq3z7cyymvygsc",
                "7bf741aa5dfc567dc3ba556e76ec36d36ccaa5b81343c7277f704050": "pool19kzx76r6a0p5vgc5jer4amy7h4jgqpru6ulfgjm94ke2yleswaf",
                "f3a63578372c8e780c05dd48eeae8b6c8b7f111bddf05c729c0373e2": "pool1sj3xltrqh6yccm99sllucdl66pd4udq7wxqdfx35y2ld5jj3lqv",
                "bf5267ca1a97d0629c08493d0ad641ba4ec0586a77a2074e907c34a9": "pool1wjkugue635ckgyfwjvur8l9uyqvtv4y0qdql4vzw8uxa6z3rhdz",
            },
        },
    }

    genesis_configuration = GenesisConfiguration(**valid_config)
    assert genesis_configuration.era == "shelley"
    assert isinstance(genesis_configuration.initial_parameters, ProtocolParameters)

    # Missing required parameter
    invalid_config = valid_config.copy()
    invalid_config.pop("era")
    with pytest.raises(TypeError):
        GenesisConfiguration(**invalid_config)
