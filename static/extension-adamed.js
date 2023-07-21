(function (Scratch) {
    "use strict";

    if (!Scratch.extensions.unsandboxed) {
        throw new Error("This extension must run unsandboxed");
    }

    fetch("http:localhost:8000/static/signatures.json")
        .then((res) => res.json())
        .then((signatures) => {
            class AdamedPicoProxy {
                getInfo() {
                    let blocks = [];

                    for (const [f_name, f_args] of Object.entries(signatures)) {
                        blocks.push({
                            opcode: f_name,
                            blockType: Scratch.BlockType.COMMAND,
                            text: f_name,
                        });
                    }

                    return {
                        id: "adamedpicoproxy",
                        name: "Adamed Pico Proxy",
                        blocks,
                    };
                }
            }

            for (const [f_name, f_args] of Object.entries(signatures)) {
                AdamedPicoProxy.prototype[f_name] = () => {
                    console.log(`Command: ${f_name}, executed!`);

                    // TODO: Executre WebSocket
                };
            }

            Scratch.extensions.register(new AdamedPicoProxy());
        })
        .catch((err) => {
            throw err;
        });
})(Scratch);
