document.addEventListener('DOMContentLoaded', function() {
    let displayElement = document.getElementById('result');
    let currentExpression = '';
    let memoryValue = 0; 

    function refreshDisplay() {
        displayElement.innerText = currentExpression || '0';
    }

    function appendToExpression(char) {
        if (currentExpression.length >= 10) return;
        currentExpression += char;
        refreshDisplay();
    }

    function performCalculation() {
        try {
            currentExpression = Function('"use strict"; return (' + currentExpression + ')')().toString();
            refreshDisplay();
        } catch (error) {
            currentExpression = '';
            displayElement.innerText = 'Error';
        }
    }

    function resetDisplay() {
        currentExpression = '';
        refreshDisplay();
    }

    function removeLastChar() {
        currentExpression = currentExpression.slice(0, -1);
        refreshDisplay();
    }

    const scientificOperations = {
        sin: (x) => Math.sin(x * Math.PI / 180),
        cos: (x) => Math.cos(x * Math.PI / 180),
        tan: (x) => Math.tan(x * Math.PI / 180),
        sqrt: (x) => Math.sqrt(x),
        square: (x) => Math.pow(x, 2),
        '1/x': (x) => 1 / x,
        pi: () => Math.PI,
        factorial: (x) => {
            let num = parseInt(x);
            let factResult = 1;
            for (let i = 1; i <= num; i++) {
                factResult *= i;
            }
            return factResult;
        }
    };

    function performScientificCalculation(operation) {
        if (operation === 'pi') {
            appendToExpression(scientificOperations.pi().toString());
        } else {
            currentExpression = scientificOperations[operation](parseFloat(currentExpression)).toString();
            refreshDisplay();
        }
    }

    function handleMemory(action) {
        const value = parseFloat(currentExpression);
        switch (action) {
            case 'mc':
                memoryValue = 0;
                break;
            case 'm+':
                memoryValue += value;
                break;
            case 'm-':
                memoryValue -= value;
                break;
            case 'mr':
                currentExpression = memoryValue.toString();
                refreshDisplay();
                break;
        }
    }

    document.querySelectorAll('td').forEach(function(cell) {
        cell.addEventListener('click', function() {
            handleInput(this.id, this.innerText);
        });
    });

    function handleInput(action, value) {
        if (value === 'Scientific') return;
        switch (action) {
            case 'Enter':
                performCalculation();
                break;
            case 'Backspace':
                removeLastChar();
                break;
            case 'c':
                resetDisplay();
                break;
            case '+':
            case '-':
            case '*':
            case '/':
                appendToExpression(action);
                break;
            case 'sin':
            case 'cos':
            case 'tan':
            case 'sqrt':
            case 'square':
            case '1/x':
            case 'pi':
            case 'factorial':
                performScientificCalculation(action);
                break;
            case 'mc':
            case 'm+':
            case 'm-':
            case 'mr':
                handleMemory(action);
                break;
            default:
                appendToExpression(value);
                break;
        }
    }
});