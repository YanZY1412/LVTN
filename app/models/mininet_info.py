# model/mininet_info.py

def get_fixed_net_info():
    return {
        "hosts": {
            "h1": {
                "ip": "10.0.0.1",
                "interfaces": {
                    "h1-eth0": {"s2": "openflow:2", "output-node-connector": 2}
                }
            },
            "h2": {
                "ip": "10.0.0.2",
                "interfaces": {
                    "h2-eth0": {"s2": "openflow:2", "output-node-connector": 3}
                }
            },
            "h3": {
                "ip": "10.0.0.3",
                "interfaces": {
                    "h3-eth0": {"s3": "openflow:3", "output-node-connector": 2}
                }
            },
            "h4": {
                "ip": "10.0.0.4",
                "interfaces": {
                    "h4-eth0": {"s3": "openflow:3", "output-node-connector": 3}
                }
            }
        },
        "switches": {
            "s1": {
                "interfaces": {
                    "s1-eth1": {"s2": "openflow:2", "output-node-connector": 1},
                    "s1-eth2": {"s3": "openflow:3", "output-node-connector": 1}
                }
            },
            "s2": {
                "interfaces": {
                    "s2-eth1": {"s1": "openflow:1", "output-node-connector": 1},
                    "s2-eth2": {"h1": "host", "output-node-connector": 0},
                    "s2-eth3": {"h2": "host", "output-node-connector": 0}
                }
            },
            "s3": {
                "interfaces": {
                    "s3-eth1": {"s1": "openflow:1", "output-node-connector": 2},
                    "s3-eth2": {"h3": "host", "output-node-connector": 0},
                    "s3-eth3": {"h4": "host", "output-node-connector": 0}
                }
            }
        },
        "controllers": ["c0"]
    }
