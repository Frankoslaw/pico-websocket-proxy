class HelloWorld {
    getInfo() {
        return {
            id: "adamed_pico_proxy",
            name: "Proxy using websockets from TurboWarp into adamed smartup rpi pico based robot.",
            blocks: [
                {
                    opcode: "hello",
                    blockType: Scratch.BlockType.REPORTER,
                    text: "Hello!",
                },
            ],
        };
    }

    hello() {
        return "World!";
    }
}

Scratch.extensions.register(new HelloWorld());
