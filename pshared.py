# coding=utf-8

class Pshared:
    def __init__(self, bits_to_index, local_history_size):
        self.bits_to_index = bits_to_index
        self.size_of_lh_table = 2**bits_to_index
        self.local_history_size = local_history_size
        self.size_of_branch_table = 2**local_history_size
        self.table_values = [0 for i in range(self.size_of_lh_table)]
        self.table_keys = [i for i in range(self.size_of_lh_table)]
        self.lh_table = dict(zip(self.table_keys, self.table_values))
        self.p_table_values = [0 for i in range(self.size_of_branch_table)]
        self.p_table_keys = [i for i in range(self.size_of_branch_table)]
        self.branch_table = dict(zip(self.p_table_keys, self.p_table_values))
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0

    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\t\tP-Shared")
        print("\tEntradas en el Predictor:\t\t\t\t"+str(2**self.bits_to_index))
        print("\tEntradas en la Historia Global:\t\t\t\t"+str(self.local_history_size))

    def print_info_tournament(self):
        print("\tSobre el predictor Local:")
        print("\t\tEntradas en el History Table:\t\t\t\t"+str(2**self.bits_to_index))
        print("\t\tTamaño de los registros de historia local:\t\t"+str(self.local_history_size))
        print("\t\tEntradas en el Pattern Table:\t\t\t\t"+str(2**self.local_history_size))

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

    def predict(self, PC):
        #last_n_bits_pc = int(PC) & ((2 ** self.bits_to_index)-1) # Mascara AND de la cantidad de bits que se quieren
        lh_hash_key = (int(PC) % self.size_of_lh_table)
        lh_table_entry = self.lh_table[lh_hash_key]
        branch_table_entry = self.branch_table[lh_table_entry]
        if branch_table_entry in [0, 1]:
            return "N"
        else:
            return "T"

    def update(self, PC, result, prediction):
        lh_hash_key = (int(PC) % self.size_of_lh_table)
        lh_table_entry = self.lh_table[lh_hash_key]
        branch_table_entry = self.branch_table[lh_table_entry]

        #Update entry accordingly
        if branch_table_entry == 0 and result == "N":
            updated_branch_table_entry = branch_table_entry  #Se mantiene porque no se  tomo

        elif branch_table_entry != 0 and result == "N":
            updated_branch_table_entry = branch_table_entry -1 # Se resta 1 por que no se tomo y aun no es 0

        elif branch_table_entry == 3 and result == "T":
            updated_branch_table_entry = branch_table_entry  # Se mantiene porque se tomo

        else:
            updated_branch_table_entry = branch_table_entry + 1 #En otro caso se tomo y aun no es 3

        self.branch_table[lh_table_entry] = updated_branch_table_entry
        
        # Update local history
        self.lh_table[lh_hash_key] = ((self.lh_table[lh_hash_key] % (2**(self.local_history_size-1))) << 1) # Si no se tomo se agrega un 0 en el LSB
        if result != "N":
            self.lh_table[lh_hash_key] +=1 

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
