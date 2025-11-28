module.exports = function beautify(code) {
    try {
        return code
            .split("\n")
            .map(line => line.trim())
            .join("\n")
            .replace(/\{/, "{\n")
            .replace(/\}/, "\n}");
    } catch (err) {
        return code;
    }
};
