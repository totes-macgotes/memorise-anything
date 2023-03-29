const backCard = 'back.png';
const frontCards = ['front1.png','front2.png','front3.png'];

let flippedCards = [];
let matchedCards = [];
let numCards = 6;
let canFlip = true;

function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

function generateGameBoard(numCards, back, fronts) {
    const gameBoard = document.getElementById('game-board');
    gameBoard.innerHTML = '';
  
    const shuffledFrontCards = shuffle(fronts.slice(0, numCards / 2).concat(fronts.slice(0, numCards / 2)));
    shuffle(shuffledFrontCards);
  
    for (let i = 0; i < 1; i++) {
      const row = document.createElement('tr');
      for (let j = 0; j < 3; j++) {
        const card = document.createElement('td');
        const cardInner = document.createElement('div');
        const cardFront = document.createElement('div');
        const cardBack = document.createElement('div');
        const imgFront = document.createElement('img');
        const imgBack = document.createElement('img');
  
        cardInner.classList.add('card');
        cardFront.classList.add('front');
        cardBack.classList.add('back');

        console.log(shuffledFrontCards.length);
        imgFront.src = shuffledFrontCards.pop();
        
        imgBack.src = back;
        imgBack.classList.add('card-image');
        cardBack.appendChild(imgBack);
        cardInner.appendChild(cardFront);
        cardInner.appendChild(cardBack);
        card.appendChild(cardInner);
  
        card.addEventListener('click', function() {
          flipCard(this);
        });
  
        row.appendChild(card);
      }
      gameBoard.appendChild(row);
    }
  }
  

function flipCard(card) {
  if (!canFlip) {
    return;
  }

  if (flippedCards.length < 2) {
    card.classList.add('flip');
    flippedCards.push(card);
  }

  if (flippedCards.length === 2) {
    canFlip = false;
    setTimeout(checkCards, 1000);
  }
}

function checkCards() {
  const card1 = flippedCards[0].querySelector('.back .card-image').src;
  const card2 = flippedCards[1].querySelector('.back .card-image').src;

  if (card1 === card2) {
    flippedCards.forEach(function(card) {
      card.removeEventListener('click', flipCard);
      card.classList.add('matched');
      matchedCards.push(card);
    });
  } else {
    flippedCards.forEach(function(card) {
      card.classList.remove('flip');
    });
  }

  flippedCards = [];
  canFlip = true;

  if (matchedCards.length === numCards) {
    setTimeout(function() {
      alert('Glückwunsch, du hast das Spiel gewonnen!');
      generateGameBoard(numCards, backCard, frontCards);
      matchedCards = [];
    }, 1000);
  }
}

generateGameBoard(numCards, backCard, frontCards);
