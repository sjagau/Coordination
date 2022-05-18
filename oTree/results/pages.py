from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants


class Coordination(Page):

    def vars_for_template(self):
        # Pulling coordination results: [type, game, [a,b,c,d], [self, other, *rd1, *rd2], payoff], *only for task==1
        num_rounds = self.session.vars['rounds_coordination']
        results_dict = self.participant.vars['results_dict']
        list_sequence = self.participant.vars['list_sequence']
        p = self.player
        # Putting problems into order experienced by participants, generating input list like as in decision interface
        tasks = []
        payoffs = []
        types = []
        a1 = []
        b1 = []
        c1 = []
        d1 = []
        a2 = []
        b2 = []
        c2 = []
        d2 = []
        inputs_own = []
        inputs_other = []
        rd1 = []
        rd2 = []
        other_As = []
        other_Bs = []
        for k in range(num_rounds):
            # Retrieving porblems in order of list sequence and labeling parameters
            l = list_sequence[k]
            results = results_dict[l]
            it_order = self.participant.vars['it_order_' + str(k+1)]
            ch_order_self = self.participant.vars['ch_order_self_' + str(k+1)]
            ch_order_other = self.participant.vars['ch_order_other_' + str(k+1)]
            # Assigning task numbers within batch, reversing where necessary
            if it_order == 1:
                task = 10-results[1]
            else:
                task = results[1]+1
            # Accounting for round number
            if k >= 2:
                task = task + (k-1)*10
            # Task numbers
            tasks.append(task)
            # Task types
            types.append(results[0])
            # Payoffs
            payoffs.append(results[4])
            setattr(p, 'payoff_' + str(k+1), results[4])
            #Finding random numbers; these will not be in iterable since only one task features paid beliefs
            if results[0]==1:
                rd1=results[3][2]
                rd2=results[3][3]
                rd_min=min(rd1,rd2)
            # Reversing labels where necessary, this accounts for all changes other than in the html itself
            permuted_results = p.permute_results(results, ch_order_self, ch_order_other)
            a1.append(permuted_results[0][0])
            b1.append(permuted_results[0][1])
            c1.append(permuted_results[0][2])
            d1.append(permuted_results[0][3])
            a2.append(permuted_results[0][4])
            b2.append(permuted_results[0][5])
            c2.append(permuted_results[0][6])
            d2.append(permuted_results[0][7])
            inputs_own.append(permuted_results[1])
            inputs_other.append(permuted_results[2])
            #Finding residual probability; will not be in iterable since only one task features paid beliefs
            if results[0]==1:
                resid = 100-permuted_results[1]
            #Changing other_labels page if equilibria are off diagonal
            if permuted_results[3] == 1:
                other_A="B"
                other_B="A"
            else:
                other_A="A"
                other_B="B"
            other_As.append(other_A)
            other_Bs.append(other_B)
        # Total points payoff
        total_points = sum(payoffs)
        p.participant.payoff = total_points        
        # Total dollar payoff
        total_dollars = p.participant.payoff.to_real_world_currency(self.session)
        total_payoff = p.participant.payoff_plus_participation_fee()
        indices = [i+1 for i in range(num_rounds)]
        min_rounds = [1,1,11]
        max_rounds = [10,10,20]
        # Zipping iterable page inputs
        page_indices = [*zip(indices, min_rounds, max_rounds)]
        page_inputs = [*zip(indices, min_rounds, max_rounds, tasks, types, a1, b1, c1, d1, a2, b2, c2, d2, inputs_own, inputs_other, other_As, other_Bs, payoffs)]
        payoff_list = [*zip(indices, payoffs)]
        # Non-iterable page inputs
        num_rounds = num_rounds
        participation_fee = self.session.config['participation_fee']
        real_equivalent = 1/self.session.config['real_world_currency_per_point']
        belief_high = self.session.vars['belief_high']
        belief_low = self.session.vars['belief_low']

        page_dict = dict(
            indices=page_indices,
            inputs=page_inputs,
            payoffs_list=payoff_list, 
            rd1=rd1,
            rd2=rd2,
            rd_min=rd_min, 
            resid=resid,
            num_rounds=num_rounds,
            total_points=total_points,
            total_dollars=total_dollars,
            total_payoff=total_payoff,
            participation_fee=participation_fee,
            real_equivalent=real_equivalent,
            belief_high=belief_high,
            belief_low=belief_low,
        )

        return page_dict


page_sequence = [
    Coordination,
]
