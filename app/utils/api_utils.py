class FlowRule:
    def __init__(self, flow_id, table_id=0, priority=100, src_ip=None, dst_ip=None, flow_name="default-flow", fw_port=None):
        self.flow_id = flow_id
        self.table_id = table_id
        self.priority = priority
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.flow_name = flow_name
        self.fw_port = fw_port

    def to_dict(self):
        match = {
            "ethernet-match": {
                "ethernet-type": {
                    "type": 2048  
                }
            }
        }

        if self.src_ip:
            match["ipv4-source"] = f"{self.src_ip}/32"
        if self.dst_ip:
            match["ipv4-destination"] = f"{self.dst_ip}/32"
        
        actions = []
        if self.fw_port: 
            actions.append({
                "order": 0,
                "output-action": {
                    "output-node-connector": self.fw_port
                }
            })
        flow = {
            "id": self.flow_id,
            "table_id": self.table_id,
            "priority": self.priority,
            "flow-name": self.flow_name,
            "cookie": "1",
            "cookie_mask": "255",
            "hard-timeout": 0,
            "idle-timeout": 0,
            "installHw": False,
            "barrier": False,
            "strict": False,
            "match": match,
            "instructions": {
                "instruction": [
                    {
                        "order": 0,
                        "apply-actions": {
                            "action": actions
                        }
                    }
                ]
            }
        }

        return {
            "flow-node-inventory:flow": [flow]
        }
