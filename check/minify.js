module.exports = function minify(code) {
    try {
        return code.replace(/\s+/g, " ").trim();
    } catch (err) {
        return code;
    }
};
