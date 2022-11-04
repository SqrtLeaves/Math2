from src.func import *

test1 = {
    f.add:[
        "b",
        {
            f.times:[
                "b", {
                    f.add: ["a","b"]
                }
            ]
        },
        {
            f.times:[
                "b","c"
            ]
        }
    ]
}


test2 = {
    f.add:[
        {
            f.times: [
                "b", {
                    f.add: ["a",
                            {f.times:[
                        "a","b"
                    ]}]
                }
            ]
        },
        {
            f.times:[
                "b","c"
            ]
        },
        "a"
    ]
}

