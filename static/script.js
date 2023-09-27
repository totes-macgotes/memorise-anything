const cards = document.querySelectorAll('.card');

const wrongPairRevealDelay = 1500;


// cards zufällig sortieren
const parent = document.getElementById('grid');
const children = Array.from(parent.children);
children.sort(() => Math.random() - 0.5);
children.forEach(child => parent.appendChild(child));

var game_mode_index = "{{ game_mode_index }}";
var game_mode_index = document.getElementById("game_mode_index").getAttribute("value");

var firstCard;
var secondCard;

var gameFrozen = false;

let sema = 0;


// Struktur: pair_id, timestamp 
var pairs = [];

// alle Karten (id + A/B) die geöffnet wurden
var cardHistory = [];

var luckyCount = 0;


for (let i = 0; i < cards.length; i++) {
    cards[i].addEventListener('click', function() {
        if(sema == 0 && cards[i].getAttribute("frozen") == "false" && firstCard != cards[i] && !gameFrozen){
            sema++;
            cards[i].classList.toggle('flip');
            if(cards[i].getAttribute("revealed") === "true"){
                cards[i].setAttribute("revealed", "false");
            } else {
                // Karte wird aufgedeckt
                cards[i].setAttribute("revealed", "true");
                
                var cardname = getCardName(cards[i]);
                cardHistory.push(cardname);


                //text - sound
                if(game_mode_index == 1){
                    if (cards[i].getAttribute('class') !== null) {
                        playSound(cards[i].getAttribute("sound"));
                    }
                }
                //random
                else if(game_mode_index == 3){
                    if (cards[i].getAttribute('class') !== null) {
                        playSound(cards[i].getAttribute("sound"));
                    }
                }

                
                if(firstCard == undefined){
                    firstCard = cards[i];
                }
                else {
                    secondCard = cards[i];

                    if(checkForPair()){
                        //pair revealed 
                        playZoomAnimation(); 
                        firstCard.setAttribute("frozen", true);
                        secondCard.setAttribute("frozen", true);

                        var timeString = document.getElementById("timer").innerHTML;
                        pairs.push({pair_id: firstCard.getAttribute("pair_id"), timestamp: timeString})


                        //lucky? 
                        past_hist = cardHistory.slice()
                        past_hist.pop()
                        past_hist.pop()
                        if(!past_hist.includes(getCardName(firstCard)) && !past_hist.includes(getCardName(secondCard))){
                            luckyCount++;
                        }

                        var allRevealed = true;
                        for (let i = 0; i < cards.length; i++) {
                            if(cards[i].getAttribute("revealed") === "false"){
                                allRevealed = false;
                            }
                        }

                        if(allRevealed){
                            pauseTimer();
                            setTimeout(function() {sendDataToGameResultsPage(timerMinutes, timerSeconds, luckyCount)}, 3000);
                        }
                    }
                    else{
                        //no pair revealed  
                        playShakeAnimation();
                        gameFrozen = true;
                        card1 = firstCard;
                        card2 = secondCard;
                        card1.setAttribute("frozen", true);
                        card2.setAttribute("frozen", true);

                        setTimeout(function() {
                            card1.classList.toggle('flip');
                            card2.classList.toggle('flip');
                            card1.setAttribute("revealed", "false");
                            card2.setAttribute("revealed", "false");

                            card1.setAttribute("frozen", false);
                            card2.setAttribute("frozen", false);

                            gameFrozen = false;
                          },wrongPairRevealDelay);
                    }
                
                   

                    firstCard = undefined;
                    secondCard = undefined;
                }
            }
            sema--;
        } else {
            //play bad sound 
            var audio = new Audio('static/cancel.mp3');
            audio.play();
        }
    });
}

function getCardName(card){
    var cardname = card.getAttribute("pair_id")
    if(card.getAttribute("cardA")  === "true"){
        cardname += "A";
    }
    else{
        cardname += "B";
    }
    return cardname;
}

function checkForPair(){
    return firstCard?.getAttribute("pair_id") === secondCard?.getAttribute("pair_id");
}

function playSound(sound){
    var audio = new Audio('static/game_files/' + sound);
    audio.play();
}

function playZoomAnimation(){
    firstCard.classList.remove('zoom-card');
    secondCard.classList.remove('zoom-card');
    firstCard.offsetWidth;
    secondCard.offsetWidth;
    firstCard.classList.add('zoom-card');
    secondCard.classList.add('zoom-card');

}

function playShakeAnimation(){
    firstCard.classList.remove('shake-card');
    secondCard.classList.remove('shake-card');
    firstCard.offsetWidth;
    secondCard.offsetWidth;
    firstCard.classList.add('shake-card');
    secondCard.classList.add('shake-card');

}

function sendDataToGameResultsPage(minutes, seconds, luckyMatches) {
    var data = {
        "minutes": minutes, 
        "seconds": seconds, 
        "lucky_matches": luckyMatches
    };

    var queryString = Object.keys(data).map(key => key + '=' + data[key]).join('&');
    window.location.href = "/game_results?" + queryString;
  }


/*function onCardRevealed(card) {
    sema++;
    const revealedCards = document.querySelectorAll('.card[revealed="true"]');
    if (revealedCards.length > 1) {
        for (let i = 0; i < revealedCards.length; i++) {
            if(revealedCards[i] != card){
                // check for pair
                setTimeout(function() {
                    turnTwoCards(card, revealedCards[i]);
                  },wrongPairRevealDelay);
            }
        }
    } else {
  
    }
    sema--;
  }

  function turnTwoCards(card1, card2) {
    sema++;
    card1.classList.toggle('flip');
    card2.classList.toggle('flip');
    sema--;
  }*/