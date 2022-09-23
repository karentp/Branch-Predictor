# coding=utf-8

from unittest import result


class Tournament:
    def __init__(self, pshared, gshared):
        self.gshared = gshared
        self.pshared = pshared
        self.meta_predictor = 0
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0

    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\t\t Tournament")
        gshared = self.gshared 
        pshared = self.pshared
        gshared.print_info_tournament()
        pshared.print_info_tournament()
        

    def print_stats(self):
        print("Resultados de la simulación")
        print("\t# branches:\t\t\t\t\t\t"+str(self.total_predictions))
        print("\t# branches tomados predichos correctamente:\t\t"+str(self.total_taken_pred_taken))
        print("\t# branches tomados predichos incorrectamente:\t\t"+str(self.total_taken_pred_not_taken))
        print("\t# branches no tomados predichos correctamente:\t\t"+str(self.total_not_taken_pred_not_taken))
        print("\t# branches no tomados predichos incorrectamente:\t"+str(self.total_not_taken_pred_taken))
        perc_correct = 100*(float(self.total_taken_pred_taken+self.total_not_taken_pred_not_taken))/float(self.total_predictions)
        formatted_perc = "{:.3f}".format(perc_correct)
        print("\t% predicciones correctas:\t\t\t\t"+str(formatted_perc)+"%")
    
    def predict_and_update(self, PC, result):
        gshared = self.gshared 
        pshared = self.pshared 
        #predict
        pshared_prediction = self.pshared.predict(PC)
        gshared_prediction = self.gshared.predict(PC)
        #update
        gshared.update(PC,result, pshared_prediction)
        pshared.update(PC,result, gshared_prediction)
        final_prediction = pshared_prediction

        if self.meta_predictor in [0,1] and pshared_prediction  != gshared_prediction:
            final_prediction = pshared_prediction
            if final_prediction != result:
                self.meta_predictor +=1
        else:
            if self.meta_predictor > 0:
                self.meta_predictor -=1

            elif self.meta_predictor in [2,3] and pshared_prediction !=gshared_prediction:
                final_prediction = gshared_prediction
                if final_prediction != result:
                    self.meta_predictor -=1
                else:
                    if self.meta_predictor <3:
                        self.meta_predictor +=1
            
            else:
                final_prediction = pshared_prediction

        
        #Update stats
        if result == "T" and result == final_prediction:
            self.total_taken_pred_taken += 1
        elif result == "T" and result != final_prediction:
            self.total_taken_pred_not_taken += 1
        elif result == "N" and result == final_prediction:
            self.total_not_taken_pred_not_taken += 1
        else:
            self.total_not_taken_pred_taken += 1

        self.total_predictions += 1



