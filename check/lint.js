module.exports = function lint(code) {
    const issues = [];
    if (!code.includes(";") && !code.includes("def ")) {
        issues.push("Possible missing semicolons");
    }
    if (code.includes("console.log") && !code.includes("use strict")) {
        issues.push("Consider using 'use strict' for cleaner JS");
    }
    if (code.length < 10) {
        issues.push("Code is too short to analyze");
    }
    return issues;
};
