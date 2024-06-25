// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function () {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

document.addEventListener('DOMContentLoaded', function () {
    var ageField = document.querySelector('select[name="age"]');
    var statusField = document.querySelector('select[name="status"]');
    var attractionsField = document.querySelector('select[name="attractions"]');
    var groupField = document.querySelector('select[name="group"]');
    var ticketPriceElement = document.getElementById('ticketPrice');

    window.saveTicket = function () {
        var ticketData = JSON.parse(localStorage.getItem('ticketData')) || [];
        var newTicket = {
            age: ageField.value,
            status: statusField.value,
            attractions: attractionsField.value,
            group: groupField.value,
            count: 1,
            price: parseFloat(ticketPriceElement.dataset.price),
        };
        ticketData.push(newTicket);
        localStorage.setItem('ticketData', JSON.stringify(ticketData));
        window.location.href = "/basket/";
    }

    function updatePrice() {
        var ageValue = ageField.value;
        var statusValue = statusField.value;
        var attractionsValue = attractionsField.value;
        var groupValue = groupField.value;

        // Логика для определения цены в зависимости от выбора
        var price = 0;
        if (statusValue === 'platinum' && ageValue === 'adult') {
            price = 3000;
        } else if (statusValue === 'platinum' && ageValue === 'child') {
            price = 2500;
          // Цена для platinum
        } else if (statusValue === 'vip') {
            if (groupValue === 'family') {
                price = 1700; // Цена для VIP с семейной группой
            } else if (groupValue === 'extrim') {
                price = 2200; // Цена для VIP с экстремальной группой
            } else if (groupValue === 'child') {
                price = 1100; // Цена для VIP с детской группой
            }
        } else if (statusValue === 'standard') {
            // Логика для стандартного статуса
            var attractionPrices = {
                'shaker': 900,
                'free': 950,
                'katap': 1100,
                'osminog': 450,
                'aviat': 450,
                'fire': 450,
                'koleso': 550,
                'katam': 650,
                'gonki': 750
            };
            price = attractionPrices[attractionsValue] || 0; // Используем цену из словаря или 0, если не найдено
        }

        // Устанавливаем текст цены в элементе на странице
        ticketPriceElement.textContent = price ? price + ' руб.' : '';
        ticketPriceElement.dataset.price = price;
    }

    function resetFields() {
        attractionsField.value = '';
        groupField.value = '';
        updatePrice();
    }

    // Функция для обновления доступности опций в зависимости от выбранного возраста и статуса
    function updateFields() {
        var ageValue = ageField.value;
        var statusValue = statusField.value;

        // Делаем опции аттракционов некликабельными в зависимости от возраста и статуса
        if (ageValue === 'adult' && statusValue === 'standard') {
            var options = attractionsField.options;
            for (var i = 0; i < options.length; i++) {
                var option = options[i];
                if (option.parentNode.label === 'Детские') {
                    option.disabled = true;
                    attractionsField.value = '';
                } else {
                    option.disabled = false;
                }
            }
        } else {
            // В остальных случаях делаем все опции доступными
            var options = attractionsField.options;
            for (var i = 0; i < options.length; i++) {
                var option = options[i];
                if (option.parentNode.label === 'Экстремальные') {
                    option.disabled = true;
                    attractionsField.value = '';
                } else {
                    option.disabled = false;
                }
            }
        }

        if (ageValue === 'adult' && statusValue === 'vip') {
            var options = groupField.options;
            for (var i = 0; i < options.length; i++) {
                var option = options[i];
                if (option.value === 'child') {
                    option.disabled = true;
                    groupField.value = '';
                } else {
                    option.disabled = false;
                }
            }
        } else {
            // В остальных случаях делаем все опции доступными
            var options = groupField.options;
            for (var i = 0; i < options.length; i++) {
                var option = options[i];
                if (option.value === 'extrim') {
                    option.disabled = true;
                    groupField.value = '';
                } else {
                    option.disabled = false;
                }
            }
        }

        // Делаем поля аттракционов и групп некликабельными при выборе Platinum
        if (statusValue === 'platinum') {
            attractionsField.disabled = true;
            groupField.disabled = true;
        } else if (statusValue === 'vip') {
            attractionsField.disabled = true;
            groupField.disabled = false;
        } else if (statusValue === 'standard') {
            attractionsField.disabled = false;
            groupField.disabled = true;
        }
    }

    // Слушаем изменения в полях возраста и статуса и обновляем доступность полей аттракционов и групп
    ageField.addEventListener('change', function () {
        resetFields(); // Сброс полей
        updateFields(); // Обновление доступности опций
        updatePrice(); // Обновление цены
    });

    statusField.addEventListener('change', function () {
        resetFields(); // Сброс полей
        updateFields(); // Обновление доступности опций
        updatePrice(); // Обновление цены
    });

    attractionsField.addEventListener('change', updatePrice);
    groupField.addEventListener('change', updatePrice);

    // Вызываем updatePrice и updateFields для начальной установки при загрузке страницы
    updatePrice();
    updateFields();
});


document.addEventListener('DOMContentLoaded', function () {
    var tickets = JSON.parse(localStorage.getItem('ticketData')) || [];
    var ticketsContainer = document.getElementById('basket-items-container');
    var totalPriceElement = document.getElementById('total-price');
    var totalCost = 0;

    var age = { 'adult': 'Взрослый', 'child': 'Детский' };
    var status = { 'standard': 'Standard', 'vip': 'VIP', 'platinum': 'Platinum' };
    var attractions = {
        'osminog': 'Осьминожка', 'fire': 'Пожарная команда', 'aviat': 'Авиаторы',
        'koleso': 'Колесо обозрения', 'katam': 'Катамараны', 'gonki': 'Крутые гонки',
        'katap': 'Катапульта', 'shaker': 'Шейкер', 'free': 'Свободное падение'
    };
    var group = { 'extrim': 'Экстремальные аттракционы', 'family': 'Семейные аттракционы', 'child': 'Детские аттракционы' };

    if (tickets.length === 0) {
        var blockOfferElem = document.querySelector('.block_offer');
        var noItemsElem = document.querySelector('.no-items');
        blockOfferElem.style.display = "none";
        noItemsElem.style.display = "flex";
    }

    tickets.forEach(function (ticket, index) {
        var ageText = age[ticket.age] || ticket.age;
        var statusText = status[ticket.status] || ticket.status;
        var attractionsText = attractions[ticket.attractions] || ticket.attractions;
        var groupText = group[ticket.group] || ticket.group;

        var ticketElement = document.createElement('div');
        ticketElement.className = 'ticket_basket';
        ticketElement.innerHTML = `
            <div class="ticket_basket">
                <ul>
                    <li>${ageText}</li>
                    <li>${statusText}</li>
                    ${ticket.status === 'standard' ? `<li>${attractionsText}</li>` : `<li>${groupText}</li>`}
                </ul>
                <div class="ticket_count">
                    <button class="count" onclick="updateCount(${index}, 'decrease')">-</button>
                    <span id="ticketCount-${index}">${ticket.count}</span>
                    <button class="count" onclick="updateCount(${index}, 'increase')">+</button>
                </div>
                <p class="ticket_price">${ticket.price} руб.</p>
                <button class="delete" onclick="removeFromCart(${index})">X</button>
            </div>
        `;
        ticketsContainer.appendChild(ticketElement);
        totalCost += ticket.count * ticket.price;
    });

    totalPriceElement.textContent = totalCost.toFixed(2); // Округление до двух знаков

    var ticketCount = tickets.length;
    var basketIcon = document.querySelector('.basket_num');
    if (ticketCount > 0) {
        basketIcon.style.display = 'flex';
        basketIcon.innerText = ticketCount;
    }
});

document.addEventListener('DOMContentLoaded', function () {
    var tickets = JSON.parse(localStorage.getItem('ticketData')) || [];
    var ticketDataInput = document.getElementById('ticketDataInput');

    if (tickets.length === 0) {
        console.log("Корзина пуста"); // Для отладки, чтобы убедиться, что данные корректно загружаются
        return;
    }

    ticketDataInput.value = JSON.stringify(tickets);
});

function updateCount(index, action) {
    var tickets = JSON.parse(localStorage.getItem('ticketData')) || [];

    var ticket = tickets[index];
    var count = ticket.count;

    if (action === 'increase') {
        count++;
    } else if (action === 'decrease' && count > 1) {
        count--;
    }

    ticket.count = count;
    localStorage.setItem('ticketData', JSON.stringify(tickets));

    const ticketCountElement = document.getElementById(`ticketCount-${index}`);
    const totalPriceElement = document.getElementById('total-price');

    if (ticketCountElement && totalPriceElement) {
        ticketCountElement.textContent = count;
        const totalCost = tickets.reduce((total, t) => total + (t.count * t.price), 0);
        totalPriceElement.textContent = totalCost.toFixed(2); // Округление до двух знаков
    }
}

function removeFromCart(index) {
    var tickets = JSON.parse(localStorage.getItem('ticketData')) || [];
    tickets.splice(index, 1); // Удаляем билет из массива по индексу
    localStorage.setItem('ticketData', JSON.stringify(tickets));
    location.reload(); // Перезагрузка страницы для обновления корзины
}




