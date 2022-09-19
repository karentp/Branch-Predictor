# coding=utf-8

class Gshared:
    def __init__(self, bits_to_index, global_history_size):
        self.bits_to_index = bits_to_index
        self.size_of_branch_table = 2**bits_to_index
        self.table_values = [0 for i in range(self.size_of_branch_table)]
        self.table_keys = [i for i in range(self.size_of_branch_table)]
        self.branch_table = dict(zip(self.table_keys, self.table_values))
        self.global_history = 0
        if global_history_size > bits_to_index:
            self.global_history_size = self.bits_to_index
        else:
            self.global_history_size = global_history_size
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0

    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\t\tG-Shared")
        print("\tEntradas en el Predictor:\t\t\t\t"+str(2**self.bits_to_index))
        print("\tEntradas en la Historia Global:\t\t\t\t"+str(2**self.global_history_size))

    def print_stats(self):
        print("Resultados de la simulación")
        print("\t# branches:\t\t\t\t\t\t"+str(self.total_predictions))
        print("\t# branches tomados predichos correctamente:\t\t"+str(self.total_taken_pred_taken))
        print("\t# branches tomados predichos incorrectamente:\t\t"+str(self.total_taken_pred_not_taken))
        print("\t# branches no tomados predichos correctamente:\t\t"+str(self.total_not_taken_pred_not_taken))
        print("\t# branches no tomados predichos incorrectamente:\t"+str(self.total_not_taken_pred_taken))
        perc_correct = 100*(self.total_taken_pred_taken+self.total_not_taken_pred_not_taken)/self.total_predictions
        formatted_perc = "{:.3f}".format(perc_correct)
        print("\t% predicciones correctas:\t\t\t\t"+str(formatted_perc)+"%")

    def predict(self, PC):
        last_n_bits_pc = int(PC) & ((2 ** self.bits_to_index)-1) # Mascara AND de la cantidad de bits que se quieren
        hash_key = last_n_bits_pc ^ self.global_history
        branch_table_entry = self.branch_table[hash_key]
        if branch_table_entry in [0, 1]:
            return "N"
        else:
            return "T"

    def update(self, PC, result, prediction):
        last_n_bits_pc = int(PC) & ((2 ** self.bits_to_index)-1) # Mascara AND de la cantidad de bits que se quieren
        hash_key = last_n_bits_pc ^ self.global_history
        branch_table_entry = self.branch_table[hash_key]

        #Update entry accordingly
        if branch_table_entry == 0 and result == "N":
            updated_branch_table_entry = branch_table_entry  #Se mantiene porque no se  tomo

        elif branch_table_entry != 0 and result == "N":
            updated_branch_table_entry = branch_table_entry -1 # Se resta 1 por que no se tomo y aun no es 0

        elif branch_table_entry == 3 and result == "T":
            updated_branch_table_entry = branch_table_entry -1 # Se mantiene porque se tomo

        else:
            updated_branch_table_entry = branch_table_entry + 1 #En otro caso se tomo y aun no es 3

        self.branch_table[hash_key] = updated_branch_table_entry
        
        # Update global history

        if result == "N":
            self.global_history = ((self.global_history & ((2 ** self.global_history_size)-1)) << 1) # Si no se tomo se agrega un 0 en el LSB
        else:
            self.global_history = ((self.global_history & ((2 ** self.global_history_size)-1)) << 1) + 1 # Si se tomo se agrega un 1 en el LSB


        #Update stats
        if result == "T" and result == prediction:
            self.total_taken_pred_taken += 1
        elif result == "T" and result != prediction:
            self.total_taken_pred_not_taken += 1
        elif result == "N" and result == prediction:
            self.total_not_taken_pred_not_taken += 1
        else:
            self.total_not_taken_pred_taken += 1

        self.total_predictions += 1